from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
import keyboards
from lexicon import LEXICON
from states import FSMAdminStates
from aiogram.fsm.context import FSMContext
from config import load_config
from functions import load_JSON, save_JSON

router = Router()
config = load_config(None)

@router.message(Command(commands='exit'), StateFilter(FSMAdminStates))
async def log_out(message: Message, state: FSMContext):
    cur = load_JSON(config.db.db_CREDENTIALS_ADMINS)
    cur[str(message.from_user.id)]['state'] = False
    save_JSON(cur, config.db.db_CREDENTIALS_ADMINS)
    await message.answer(text=LEXICON['/exit'])
    await state.clear()

@router.message(Command(commands='cancel'), StateFilter(FSMAdminStates))
async def cancel(message: Message, state: FSMContext):
    await state.set_state(FSMAdminStates.admin_default)
@router.message(StateFilter(FSMAdminStates.change_password_a))
async def new_password(message: Message, state: FSMContext):
    cur = load_JSON(config.db.db_PASSWORDS)
    cur['admin'] = message.text
    save_JSON(cur, config.db.db_PASSWORDS)
    await message.answer('Пароль успешно изменён')
    await state.set_state(FSMAdminStates.admin_default)


@router.message(StateFilter(FSMAdminStates.admin_default), F.text == "Настроить пароль для администраторов")
async def user_change_password(message: Message, state: FSMContext):
    await message.answer('Введите новый пароль')
    await state.set_state(FSMAdminStates.change_password_a)


@router.message(StateFilter(FSMAdminStates.change_password_u))
async def new_password(message: Message, state: FSMContext):
    cur = load_JSON(config.db.db_PASSWORDS)
    cur['user'] = message.text
    save_JSON(cur, config.db.db_PASSWORDS)
    await message.answer('Пароль успешно изменён')
    await state.set_state(FSMAdminStates.admin_default)
@router.message(StateFilter(FSMAdminStates.admin_default), F.text=="Настроить пароль для преподавателей")
async def user_change_password(message: Message, state: FSMContext):
    await message.answer('Введите новый пароль')
    await state.set_state(FSMAdminStates.change_password_u)

@router.message(StateFilter(FSMAdminStates.admin_default))
async def admin_panel_init(message: Message, state: FSMContext):
    await message.answer('Используйте кнопки для навигации или напишите задачу текстом',
                         reply_markup=keyboards.admin_kb)