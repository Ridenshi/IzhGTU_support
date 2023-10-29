from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from config import load_config

config = load_config(None)
bot_token = config.tg_bot.token

# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Здраствуйте!\nЧем я могу вам помочь?\n')

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('WIP')

# Этот хэндлер будет срабатывать на отправку боту фото
@dp.message(F.photo)
async def send_photo_echo(message: Message):
    await message.answer('WIP')

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)