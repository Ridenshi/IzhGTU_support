from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm import state
import keyboards
from lexicon import LEXICON, TOPICS, DOWN_TOPICS, DOWN_DOWN_TOPICS, FAQ, YesNo
from users import USERS, ADMINS
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from states import FSMUserRegTypes, FSMAdminStates, FSMUserStates
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize, KeyboardButton)
from admin_handlers import admin_panel_init
router = Router()


# Этот хэндлер будет срабатывать на команду /start в стандартном состоянии
@router.message(Command(commands='start'))
async def process_fillform_command(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in ADMINS:
        # Если нужно добавить авторизацию для сотр.
        await message.answer(text='Вы авторизованы, как сотрудник технической поддерки')
        await state.set_state(FSMAdminStates.admin_default)
        await admin_panel_init()
    else:
        if message.from_user.id not in USERS:
            await user_register(message, state)
        else:
            # Если нужно добавить авторизацию для препод.
            await message.answer(text='Вы авторизованы, как преподаватель')
            await state.set_state(FSMUserStates.user_default)
            await user_panel_init(message)


# Регистрация новых пользователей
async def user_register(message: Message, state: FSMContext):
    await message.answer(text='Вы не зарегистрированы в системе\n\nЖелаете начать регистрацию сейчас?')
    # TODO Добавить продолжение регистрации
    # Либо добавить условных преподов и поддержку в users,
    # либо дать им общий пароль для регистрации именно как преподавателей/сотрудников


async def user_panel_init(message: Message):
    await message.answer('Используйте кнопки для навигации или напишите задачу текстом', reply_markup=keyboards.user_kb)


# Переделать чтобы реагировал только на Создать заявку
@router.message(F.text.lower() == "создать заявку",
                StateFilter(FSMUserStates.user_default))
async def user_request_start(message: Message, state: FSMContext):
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in TOPICS]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    # Отправляем пользователю сообщение с кнопками
    await message.answer(
        text='Выберите тему неполадки\n\nЕсли темы ниже не подходят введите тему вашей проблемы текстом',
        reply_markup=kb_builder.as_markup()
    )
    await state.set_state(FSMUserStates.choose_topic)


@router.message(F.text.lower() == "мои заявки",
                StateFilter(FSMUserStates.user_default))
async def user_request_start(message: Message, state: FSMContext):
    ...


@router.message(F.text.lower() == "Настройки аккаунта",
                StateFilter(FSMUserStates.user_default))
async def user_request_start(message: Message, state: FSMContext):
    ...


async def user_request_down_topics(callback: CallbackQuery, state: FSMContext):
    kb_builder = InlineKeyboardBuilder()  # создаем билдер
    data = await state.get_data()
    buttons = [InlineKeyboardButton(text=topic, callback_data=topic) for topic in
               DOWN_TOPICS[data['topic']]]  # создаем список кнопок
    kb_builder.row(*buttons, width=2)  # добавляем кнопки в билдер
    # Отправляем пользователю сообщение с кнопками
    await callback.message.answer(
        text='Выберите подтему неполадки',
        reply_markup=kb_builder.as_markup()
    )


@router.message(StateFilter(FSMUserStates.fill_context))
async def context_filling(message: Message, state: FSMContext):
    await send_request(message, state)


async def send_request(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text='Запрос отправлен\nЧтобы написать новый запрос используйте кнопку Создать запрос')
    await state.set_state(FSMUserStates.user_default)


# Реагирует на нажатие кнопок тем
@router.callback_query()
async def catch_callback_data(callback: CallbackQuery, state: FSMContext):
    # запись инфы о темах и переход в следующее состояние/функцию
    if await state.get_state() == FSMUserStates.choose_topic:
        await state.update_data(topic=callback.data)
        await state.set_state(FSMUserStates.choose_down_topic)
        await user_request_down_topics(callback, state)
    elif await state.get_state() == FSMUserStates.choose_down_topic:
        await state.set_state(FSMUserStates.fill_context)
        await callback.message.answer(text='Опишите подробно проблему (при каких обстоятельствах обнаружена проблема, '
                                           'инвентарный код и т.д.)\nНапишите ответ одним сообщением')

