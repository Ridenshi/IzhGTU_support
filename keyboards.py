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
            KeyboardButton(text="Мои заявки"),
            KeyboardButton(text="Настройки аккаунта")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Просмотреть заявки")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)
