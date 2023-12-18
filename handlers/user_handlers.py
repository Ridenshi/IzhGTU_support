from aiogram import Router, F
from lexicon import LEXICON, TOPICS, DOWN_TOPICS, FAQ, YesNo
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from functions import load_JSON, save_JSON, save_request
from config import load_config
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from states import FSMUserStates

config = load_config(None)
credentials_users = load_JSON(config.db.db_CREDENTIALS_USERS)


def is_user(message: Message) -> bool:
    credentials_users = load_JSON(config.db.db_CREDENTIALS_USERS)
    return credentials_users[str(message.from_user.id)]['state']


router = Router()


class FSMFillForm(StatesGroup):
    fill_login = State()  # Состояние ожидания ввода логина
    fill_password = State()  # Состояние ожидания ввода пароля
    fill_topic = State()  # Состояние ожидания выбора темы косяка
    fill_over_topic = State()  # состояние ожидание ввода иной темы косяка
    fill_desc = State()  # Состояние ожидания ввода описания
    down_topic_selection = State()  # Состояние ожидания ввода подтемы
    down_down_topic_selection = State()  # Состояние ожидания ввода подтемы
    faq = State()  # Состояние вывода faq
    fill_request = State()  # Состояние составления запроса в поддержку
    send_request = State()  # Состояние отправки запроса
    faq_select = State()


# Срабатывает при выходе
@router.message(Command(commands='exit'), StateFilter(FSMUserStates))
async def log_out(message: Message, state: FSMContext):
    cur = load_JSON(config.db.db_CREDENTIALS_USERS)
    cur[str(message.from_user.id)]['state'] = False
    save_JSON(cur, config.db.db_CREDENTIALS_USERS)
    await message.answer(text=LEXICON['/exit'])
    await state.clear()

@router.message(Command(commands='cancel'), StateFilter(FSMUserStates))
async def cancel(message: Message, state: FSMContext):
    await state.set_state(FSMUserStates.user_default)
async def send_request(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    save_request(str(credentials_users[str(message.from_user.id)]['name']), data['topic'], data['down_down_topic'],
                 data['description'])
    await message.answer(text='Запрос отправлен\nЧтобы написать новый запрос введите команду /help')
    await state.set_state(FSMUserStates.user_default)


@router.message(F.text.lower() == "создать заявку",
                StateFilter(FSMUserStates.user_default), is_user)
async def user_request_start(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.fill_topic)
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in TOPICS]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    # Отправляем пользователю сообщение с кнопками
    await message.answer(
        text='Выберите тему неполадки',
        reply_markup=kb_builder.as_markup()
    )
    await state.set_state(FSMUserStates.choose_topic)


@router.message(F.text.lower() == "изменить имя",
                StateFilter(FSMUserStates.user_default))
async def user_request_start(message: Message, state: FSMContext):
    await state.set_state(FSMUserStates.fill_name)
    await message.answer("Введите своё полное имя одним сообщением")


@router.message(StateFilter(FSMUserStates.fill_name))
async def user_request_continue(message: Message, state: FSMContext):
    cur = load_JSON(config.db.db_CREDENTIALS_USERS)
    cur[str(message.from_user.id)]['name']=message.text
    save_JSON(cur, config.db.db_CREDENTIALS_USERS)
    await message.answer(f"Ваше имя изменено, теперь вы {message.text}")
    await state.set_state(FSMUserStates.user_default)


@router.message(StateFilter(FSMFillForm.send_request))
async def process_send_request(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    save_request(str(credentials_users[str(message.from_user.id)]['name']), data['topic'], data['down_topic'],
                 data['description'])
    await message.answer(text='Запрос отправлен\nЧтобы написать новый запрос введите команду /help')
    await state.set_state(default_state)


async def down_topic_selection(callback: CallbackQuery, state: FSMContext):
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    data = await state.get_data()
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in
               DOWN_TOPICS[data['topic']]]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    # Отправляем пользователю сообщение с кнопками
    await callback.message.answer(
        text='Укажите подтему неполадки',
        reply_markup=kb_builder.as_markup()
    )
    # Устанавливаем состояние ожидания выбора подтемы
    # await state.set_state(FSMFillForm.down_down_topic_selection)


# Обрабатывает нажатия на inline кнопки
@router.callback_query(is_user)
async def catch_callback_data(callback: CallbackQuery, state: FSMContext):
    # запись инфы о темах и переход в следующее состояние/функцию
    if await state.get_state() == FSMUserStates.choose_topic:
        await state.update_data(topic=callback.data)
        await state.set_state(FSMFillForm.down_topic_selection)
        await down_topic_selection(callback, state)
    elif await state.get_state() == FSMFillForm.down_topic_selection:
        await state.update_data(down_topic=callback.data)
        await process_faq_sent(state, callback)
    elif await state.get_state() == FSMFillForm.fill_request:
        await state.update_data(confirmation=callback.data)
        await process_fill_request(callback, state)


async def process_faq_sent(state: FSMContext, callback: CallbackQuery):
    data = await state.get_data()
    if data['down_topic'] in FAQ:
        kb_builder = InlineKeyboardBuilder()  # создаем билдер
        buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in YesNo]  # создаем список кнопок
        kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
        mess = (FAQ[data['down_topic']])
        await callback.message.answer(text=mess)
        await callback.message.answer(
            text='Это помогло справиться с вашей проблемой?\n',
            reply_markup=kb_builder.as_markup()
        )
        await state.set_state(FSMFillForm.fill_request)
    else:
        await nofaq(callback, state)


async def process_fill_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['confirmation'] == 'Нет':
        await callback.message.answer('Опишите подробно проблему (при каких обстоятельствах обнаружена проблема, '
                                      'инвентарный код и т.д.)\nНапишите ответ одним сообщением')
        await state.set_state(FSMFillForm.send_request)
    else:
        await callback.message.answer('Запрос отменён\nЧтобы написать новый запрос введите команду /help')
        await state.set_state(FSMUserStates.user_default)


async def nofaq(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Опишите подробно проблему (при каких обстоятельствах обнаружена проблема, '
                                  'инвентарный код и т.д.)\nНапишите ответ одним сообщением')
    await state.set_state(FSMFillForm.send_request)
