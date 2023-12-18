from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from states import FSMGuestStates, FSMAdminStates, FSMUserStates
from aiogram.fsm.context import FSMContext
from functions import load_JSON, save_JSON, add_user
from config import load_config
import keyboards

router = Router()
config = load_config(None)
credentials_users = load_JSON(config.db.db_CREDENTIALS_USERS)
credentials_admins = load_JSON(config.db.db_CREDENTIALS_ADMINS)
passwords = load_JSON(config.db.db_PASSWORDS)


async def user_panel_init(message: Message):
    await message.answer('Используйте кнопки для навигации или напишите задачу текстом', reply_markup=keyboards.user_kb)


async def admin_panel_init(message: Message):
    await message.answer('Используйте кнопки для навигации или напишите задачу текстом', reply_markup=keyboards.admin_kb)

@router.message(Command(commands='start'))
async def guess_check(message: Message, state: FSMContext):
    # await state.clear()
    credentials_users = load_JSON(config.db.db_CREDENTIALS_USERS)
    credentials_admins = load_JSON(config.db.db_CREDENTIALS_ADMINS)
    if str(message.from_user.id) not in credentials_users or not credentials_users[str(message.from_user.id)].get(
            'state'):
        await message.answer(text='Здраствуйте, для начала работы введите ваш пароль')
        await state.set_state(FSMGuestStates.password)
    elif str(message.from_user.id) not in credentials_admins or not credentials_admins[str(message.from_user.id)].get(
            'state'):
        await message.answer(text='Здраствуйте, для начала работы введите ваш пароль')
        await state.set_state(FSMGuestStates.password)
    # else:
    #     cur = load_JSON(config.db.db_CREDENTIALS_ADMINS)
    #     await message.answer(
    #         f'Здраствуйте, {cur[str(message.from_user.id)].get("name")}\nВы авторизованы, как сотрудник технической '
    #         f'поддерки')
    #     await admin_panel_init(message)
    #     await state.set_state(FSMAdminStates.admin_default)


# @router.message(StateFilter(FSMGuestStates.login))
# async def process_login_sent(message: Message, state: FSMContext):
#     state.update_data(login=str(message.from_user.id))
#     if str(message.from_user) not in credentials:
#         await message.answer(text='Такого пользователя не существует\nПопробуйте ещё раз')
#     else:
#         await message.answer(text='А теперь введите ваш пароль')
#         await state.set_state(FSMGuestStates.password)

@router.message(Command(commands='cancel'), StateFilter(FSMGuestStates))
async def cancel(message: Message, state: FSMContext):
    await state.set_state(FSMGuestStates.guest_default)
@router.message(StateFilter(FSMGuestStates.password))
async def process_fill_password(message: Message, state: FSMContext):
    if passwords['user'] == str(message.text):
        if str(message.from_user.id) not in credentials_users:
            add_user(str(message.from_user.id), False, "Безымянный")
        cur = load_JSON(config.db.db_CREDENTIALS_USERS)
        cur[str(message.from_user.id)]['state'] = True
        save_JSON(cur, config.db.db_CREDENTIALS_USERS)
        await message.answer(f'Здраствуйте, {cur[str(message.from_user.id)].get("name")}\nВы авторизованы, как '
                             f'преподаватель')
        await user_panel_init(message)
        await state.set_state(FSMUserStates.user_default)
    elif passwords['admin'] == str(message.text):
        if str(message.from_user.id) not in credentials_admins:
            add_user(str(message.from_user.id), True, "Безымянный")
        cur = load_JSON(config.db.db_CREDENTIALS_ADMINS)
        cur[str(message.from_user.id)]['state'] = True
        save_JSON(cur, config.db.db_CREDENTIALS_ADMINS)
        await message.answer(
            f'Здраствуйте, {cur[str(message.from_user.id)].get("name")}\nВы авторизованы, как сотрудник технической '
            f'поддерки')
        await admin_panel_init(message)
        await state.set_state(FSMAdminStates.admin_default)
    else:
        await message.answer(
            text='Неверный пароль\n'
                 'Введите пароль снова\n'
        )
