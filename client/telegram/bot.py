from aiogram import Bot, Dispatcher, executor, types
import asyncio
from load_all import dp
import handlers
from config import ADMIN_ID
from datetime import datetime, timezone

async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand("help", "Instruction"),
    ])

async def on_shutdown(dp: Dispatcher):
    await dp.bot.close()


async def on_startup(dp: Dispatcher):
    await dp.bot.send_message(
        ADMIN_ID, 
        f"Bot 'SmartHeart' started at {datetime.now(timezone.utc)}",
        disable_notification=True)
    await set_default_commands(dp.bot)
    

# запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(handlers.wait_query())
    loop.create_task(handlers.scheduler())
    executor.start_polling(
        dp, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup, loop=loop)
