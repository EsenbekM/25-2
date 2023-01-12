from aiogram import Dispatcher, Bot
from decouple import config


TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
ADMINS = (5367214519, )
