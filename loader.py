import os
import pickle
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import bot_token
data = pickle.load(open('data/data.dat', 'rb'))
if os.stat('data/data.dat').st_size == 674:
  bot = Bot(token = bot_token, parse_mode=types.ParseMode.HTML)
  dp = Dispatcher(bot, storage=MemoryStorage())
else:
  bot = None
  dp = None
  print('Файл data.dat поврежден !')
