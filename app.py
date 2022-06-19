from aiogram import executor
from aiogram.dispatcher import FSMContext
from loader import dp
import handlers
#from utils.notify_admins import on_startup_notify



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
