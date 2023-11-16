from aiogram import Router, F
from lexicon import LEXICON
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

router = Router()

class FSMFillForm(StatesGroup):
    fill_login = State()  # Состояние ожидания ввода логина
    fill_password = State()  # Состояние ожидания ввода пароля
    fill_topic = State()  # Состояние ожидания выбора темы косяка
    fill_over_topic = State()  # состояние ожидание ввода иной темы косяка
    # upload_photo = State()     # Состояние ожидания загрузки фото
    fill_desc = State()  # Состояние ожидания ввода описания
    fill_down_topic = State()  # Состояние ожидания ввода подтемы
    faq = State()  # Состояние вывода faq
    fill_request = State()  # Состояние составления запроса в поддержку
    send_request = State()  # Состояние отправки запроса


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fill_login
@router.message(Command(commands='start'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваш логин')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_login)


@router.message(StateFilter(FSMFillForm.fill_login), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # await state.update_data(name=message.text) - проверку на имя надо
    await message.answer(text='Спасибо!\n\nА теперь введите ваш пароль')
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMFillForm.fill_topic)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_password))  # придумай как проверить что пароль от заданного логина
async def warning_not_name(message: Message):  # название функции придумай подходящее
    await message.answer(
        text='Данные, введенные вами некорректны\n\n'
             'Пожалуйста, перепроверьте, и введите новые данные\n\n'  # хуйня текст
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если введены кооректные данные
# и переводить в состояние выбора темы
@router.message(StateFilter(FSMFillForm.fill_topic))
async def process_age_sent(message: Message, state: FSMContext):  # название функции меняй
    # Cохраняем возраст в хранилище по ключу "topic" - добавь в лексикон
    await state.update_topic(topic=message.text)
    # Создаем объекты инлайн-кнопок
    printer_button = InlineKeyboardButton(
        text='Принтер',
        callback_data='printer'
    )
    pc_button = InlineKeyboardButton(
        text='Компьтер',
        callback_data='pc'
    )
    # остальное надо как то распределить
    undefined_button = InlineKeyboardButton(
        text='Пока не ясно',
        callback_data='undefined_topic'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [printer_button, pc_button],
        [undefined_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Здравствуйте!\n\nУкажите тему неполадки',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора темы
    await state.set_state(FSMFillForm.fill_topic)

# @router.message(StateFilter(FSMFillForm.faq))
# async def process_name_sent(message: Message, state: FSMContext):
#     await message.answer() тут выводим faq по выбранной подтеме
# И добавляем кнопки: вопрос решён и создать запрос в поддержку(ставим состояние fill_request)

# @router.message(StateFilter(FSMFillForm.fill_request))
# async def process_name_sent(message: Message, state: FSMContext):
#     await message.answer() задаём вопросы по шаблону
# 2 кнопки: отменить запрос и отправить(ставим состояние send_request)

# @router.message(StateFilter(FSMFillForm.send_request))
# async def process_name_sent(message: Message, state: FSMContext):
#     отправляем запрос и заканчиваем сессию
