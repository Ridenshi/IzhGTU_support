import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from handlers import admin_handlers, user_handlers


async def main() -> None:
    # Настройка бота
    config = load_config(None)
    bot = Bot(token=config.tg_bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключение роутеров для разных целей
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    # Позволяет не реагировать на апдейты присланные за время отключенного бота
    # Не спамит ответы на несколько команд /start
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск бота
    await dp.start_polling(bot)

# Запуск асинхронной функции main() в начале
if __name__ == '__main__':
    asyncio.run(main())
