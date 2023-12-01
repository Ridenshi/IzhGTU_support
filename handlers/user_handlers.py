from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm import state
from lexicon import LEXICON, TOPICS, DOWN_TOPICS, DOWN_DOWN_TOPICS, FAQ, YesNo
from users import USERS
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize, KeyboardButton)

router = Router()

#TODO кнопки располагаются в произвольном порядке, пересмотреть имеющиеся состояния

class FSMFillForm(StatesGroup):
    fill_login = State()  # Состояние ожидания ввода логина
    fill_password = State()  # Состояние ожидания ввода пароля
    fill_topic = State()  # Состояние ожидания выбора темы косяка
    fill_over_topic = State()  # состояние ожидание ввода иной темы косяка
    # upload_photo = State()     # Состояние ожидания загрузки фото
    fill_desc = State()  # Состояние ожидания ввода описания
    down_topic_selection = State()  # Состояние ожидания ввода подтемы
    down_down_topic_selection = State()  # Состояние ожидания ввода подтемы
    faq = State()  # Состояние вывода faq
    fill_request = State()  # Состояние составления запроса в поддержку
    send_request = State()  # Состояние отправки запроса
    faq_select = State()

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fill_login
@router.message(Command(commands='start'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id not in USERS:
        await message.answer(text='Вы не зарегистрированы в системе')
    else:
        if USERS[message.from_user.id]['log_in']:
            # Переходим к выбору тем
            await state.set_state(FSMFillForm.fill_topic)
            await topic_selection(message, state)
        else:
            await message.answer(text='Пожалуйста, введите ваш логин')
            # Устанавливаем состояние ожидания ввода имени
            await state.set_state(FSMFillForm.fill_login)

#Срабатывает при выходе из сессии, т.е. из аккаунта
@router.message(Command(commands='exit'))
async def log_out(message: Message, state: FSMContext):
    USERS[message.from_user.id]['log_in'] = False
    await message.answer(text=LEXICON['/exit'])
    await state.clear()

@router.message(StateFilter(FSMFillForm.fill_login))
async def process_login_sent(message: Message, state: FSMContext):
    if USERS[message.from_user.id]['login'] != message.text:
        await message.answer(text='Такого пользователя не существует\nПопробуйте ещё раз')
    else:
        await message.answer(text='Спасибо!\nА теперь введите ваш пароль')
        # Устанавливаем состояние ожидания ввода пароля
        await state.set_state(FSMFillForm.fill_password)

@router.message(StateFilter(FSMFillForm.fill_password))
async def process_fill_password(message: Message, state: FSMContext):
    if USERS[message.from_user.id]['password'] != message.text:
        await message.answer(
            text='Неверный пароль\n'
                'Введите пароль снова\n'
                'Если вы хотите прервать заполнение анкеты - '
                'отправьте команду /cancel'
       )
    else:
        USERS[message.from_user.id]['log_in'] = True
        #переходим к следующему состоянию
        #await state.set_state(FSMFillForm.fill_topic)
        await topic_selection(message, state)

@router.message(StateFilter(FSMFillForm.fill_topic))
async def topic_selection(message: Message, state: FSMContext):
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in TOPICS]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    # Отправляем пользователю сообщение с кнопками
    await message.answer(
        text='Укажите тему неполадки',
        reply_markup=kb_builder.as_markup()
    )


#@router.callback_query(StateFilter(FSMFillForm.down_topic_selection))
async def down_topic_selection(callback: CallbackQuery, state: FSMContext):
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    data = await state.get_data()
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in DOWN_TOPICS[data['topic']]]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    # Отправляем пользователю сообщение с кнопками
    await callback.message.answer(
        text='Укажите подтему неполадки',
        reply_markup=kb_builder.as_markup()
    )
    # Устанавливаем состояние ожидания выбора подтемы
    await state.set_state(FSMFillForm.down_down_topic_selection)

# отвечает на нажатие любой кнопки
@router.callback_query()
async def catch_callback_data(callback: CallbackQuery, state: FSMContext):
    # запись инфы о темах и переход в следующее состояние/функцию
    if await state.get_state() == FSMFillForm.fill_topic:
        await state.update_data(topic=callback.data)
        await state.set_state(FSMFillForm.down_topic_selection)
        await down_topic_selection(callback, state)
    elif await state.get_state() == FSMFillForm.down_down_topic_selection:
        await state.update_data(down_topic=callback.data)
        await down_down_selection(callback=callback, state=state)
    elif await state.get_state() == FSMFillForm.fill_request:
        await state.update_data(confirmation=callback.data)
        await process_fill_request(callback, state)


async def down_down_selection(state: FSMContext, callback: CallbackQuery):
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    data = await state.get_data()
    if(data['down_topic'] in DOWN_DOWN_TOPICS):
        # buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in
        #            DOWN_TOPICS[data['topic']]]  # создаем список кнопок
        # kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
        # # Отправляем пользователю сообщение с кнопками
        await callback.answer(
            text='Укажите подтему неполадки',
            reply_markup=kb_builder.as_markup()
        )
    else:
        await state.set_state(FSMFillForm.faq)
        await state.update_data(down_down_topic=data['down_topic'])
        await process_faq_sent(state=state, callback=callback)

@router.message(StateFilter(FSMFillForm.faq))
async def process_faq_sent(state: FSMContext, callback: CallbackQuery):
    data = await state.get_data()
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in YesNo]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    for x in range(0, len(FAQ[data['down_down_topic']]), 4096):
        mess = FAQ[data['down_down_topic']][x: x + 4096]
        await callback.message.answer(text=mess)
    await callback.message.answer(
        text='Это помогло справиться с вашей проблемой?\nЕсли нет, то подтвердите отправление запроса',
        reply_markup=kb_builder.as_markup()
    )
    await state.set_state(FSMFillForm.fill_request)

#@router.message(StateFilter(FSMFillForm.fill_request))
async def process_fill_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['confirmation']=='Отправить':
        await callback.message.answer('Запрос отправлен, ожидайте')
    else:
        await callback.message.answer('Запрос отменён')#
        await state.set_state(default_state)
    # @router.message(StateFilter(FSMFillForm.send_request))
    # async def process_name_sent(message: Message, state: FSMContext):
    # отправляем запрос и заканчиваем сессию
