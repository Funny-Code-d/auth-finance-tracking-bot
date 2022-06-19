from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from modules.api import ApiInterface
from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN")
API_SYSTEM_TOKEN = getenv("API_SYSTEM_TOKEN")

interface = ApiInterface(API_SYSTEM_TOKEN)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
