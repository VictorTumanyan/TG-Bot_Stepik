# URL = https://api.telegram.org/bot6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE/
# chat_id= 6325704944

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F


import requests

API_URL = 'http://api.telegram.org/bot'
BOT_TOKEN = '6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE'

CHAT_ID = 6325704944
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Ну здарова, вот ты и попался')

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Что тебе помочь то?\n'
        'Просто пишешь сообщение - я тебе отправляю его же'
    )

@dp.message(Command(commands=['cat']))
async def process_cat_command(message: Message):
    cat_response = requests.get(API_CATS_URL)

    if cat_response.status_code == 200:
        cat_url = cat_response.json()[0]['url']
        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={CHAT_ID}&photo={cat_url}&caption={"I am a cute cat :)"}')
    else:
        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={"Кажется, где-то произошла ошибочка"}')

@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text = 'Данный тип апдейтов не поддерживается методом send_copy'
        )


if __name__ == "__main__":
    dp.run_polling(bot)