from dotenv import load_dotenv
import os
from aiogram import Bot


load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
DEBUG = bool(os.getenv('DEBUG'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Создаем объект бота
bot = Bot(token=BOT_TOKEN)
PHOTO_LIMIT = 5