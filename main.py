async def on_startup(dp):
    import filters
    import asyncio
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    from utils.other import starter, user_checker
    await starter(dp)
    print("Бот запущен")
    asyncio.create_task(user_checker())
if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)
