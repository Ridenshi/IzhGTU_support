from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functions import load_JSON
import keyboards
from lexicon import LEXICON
from states import FSMAdminStates, FSMUserStates
from aiogram.fsm.context import FSMContext
from config import load_config

router = Router()


@router.message(StateFilter(FSMAdminStates.admin_default))
async def admin_panel_init(message: Message, state: FSMContext):
    await message.answer('Используйте кнопки для навигации или напишите задачу текстом',
                         reply_markup=keyboards.admin_kb)


@router.message(StateFilter(FSMAdminStates.admin_default))
async def user_request_start(message: Message, state: FSMContext):
    # TODO изменить пароль преподователей, на пароль из сообщения
    ...
    await state.set_state(FSMAdminStates.admin_default)