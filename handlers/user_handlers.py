from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon import LEXICON

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/start'])

# Этот хэндлер будет срабатывать на отправку боту фото
@router.message(F.photo)
async def send_photo_echo(message: Message):
    await message.answer(text=LEXICON['photo'])

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    await message.answer(text=LEXICON['request'])