from aiogram import Bot, Dispatcher
import logging
import aioredis as rd
# from redis import StrictRedis as rd
import config


redis = rd.from_url(config.REDIS_URL)
# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)