from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from states import FSMGuestStates
from aiogram.fsm.context import FSMContext
from functions import load_JSON, save_JSON, add_user
from config import load_config




router = Router()
config = load_config(None)
credentials_users = load_JSON(config.db.db_CREDENTIALS_USERS)
credentials_admins = load_JSON(config.db.db_CREDENTIALS_ADMINS)
passwords = load_JSON(config.db.db_PASSWORDS)

@router.message(Command(commands='start'))
async def guess_check(message: Message, state: FSMContext):
    await state.clear()
    credentials_users = load_JSON(config.db.db_CREDENTIALS_USERS)
    credentials_admins = load_JSON(config.db.db_CREDENTIALS_ADMINS)
    if str(message.from_user.id) not in credentials_users or not credentials_users[str(message.from_user.id)].get('state'):
        await message.answer(text='Здраствуйте, для начала работы введите ваш пароль')
        await state.set_state(FSMGuestStates.password)
    elif str(message.from_user.id) not in credentials_admins or not credentials_admins[str(message.from_user.id)].get('state'):
        await message.answer(text='Здраствуйте, для начала работы введите ваш пароль')
        await state.set_state(FSMGuestStates.password)

# @router.message(StateFilter(FSMGuestStates.login))
# async def process_login_sent(message: Message, state: FSMContext):
#     state.update_data(login=str(message.from_user.id))
#     if str(message.from_user) not in credentials:
#         await message.answer(text='Такого пользователя не существует\nПопробуйте ещё раз')
#     else:
#         await message.answer(text='А теперь введите ваш пароль')
#         await state.set_state(FSMGuestStates.password)

@router.message(StateFilter(FSMGuestStates.password))
async def process_fill_password(message: Message, state: FSMContext):
    if passwords['user'] == str(message.text):
        if str(message.from_user.id) not in credentials_users:
            add_user(str(message.from_user.id), False, "Безымянный")
        cur = load_JSON(config.db.db_CREDENTIALS_USERS)
        cur[str(message.from_user.id)]['state'] = True
        save_JSON(cur, config.db.db_CREDENTIALS_USERS)
        await message.answer(f'Здраствуйте, {cur[str(message.from_user.id)].get("name")}\nЧтобы начать заполнение запроса, наберите /help или воспользуйтесь меню')
        await state.clear()
    elif passwords['admin'] == str(message.text):
        if str(message.from_user.id) not in credentials_admins:
            add_user(str(message.from_user.id), True, "Безымянный")
        cur = load_JSON(config.db.db_CREDENTIALS_ADMINS)
        cur[str(message.from_user.id)]['state'] = True
        save_JSON(cur, config.db.db_CREDENTIALS_ADMINS)
        await message.answer(f'Здраствуйте, {cur[str(message.from_user.id)].get("name")}\nЧтобы начать, воспользуйтесь меню')
        await state.clear()
    else:
        await message.answer(
            text='Неверный пароль\n'
                 'Введите пароль снова\n'
        )