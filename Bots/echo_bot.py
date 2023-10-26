# URL = https://api.telegram.org/bot6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE/
# chat_id= 6325704944

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

API_URL = 'http://api.telegram.org/bot'
BOT_TOKEN = '6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Ну здарова, вот ты и попался')

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Что тебе помочь то?'
        'Просто пишешь сообщение - я тебе отправляю его же'
    )

@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)