import asyncio
from aiogram import Bot, Dispatcher
from config import load_config
from handlers import admin_handlers, user_handlers


async def main() -> None:
    config = load_config(None)
    bot = Bot(token = config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())