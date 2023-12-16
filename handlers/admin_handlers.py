from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message

import keyboards
from lexicon import LEXICON
from states import FSMAdminStates, FSMUserStates
from aiogram.fsm.context import FSMContext

router = Router()

# TODO Добавить хендлеры для просмотра (управления) заявками


@router.message(StateFilter(FSMAdminStates.admin_default))
async def admin_panel_init(message: Message, state: FSMContext):
    await message.answer('Используйте кнопки для навигации или напишите задачу текстом', reply_markup=keyboards.admin_kb)


@router.message(F.text.lower() == "Просмотреть заявки",
                StateFilter(FSMAdminStates.admin_default))
async def user_request_start(message: Message, state: FSMContext):
    ...
