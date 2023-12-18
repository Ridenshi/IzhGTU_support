from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать заявку"),
            KeyboardButton(text="Изменить имя")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Настроить пароль для преподавателей")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

request_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пред."),
            InlineKeyboardButton(text="След.")
        ]
    ]
)