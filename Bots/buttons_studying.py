from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.types.web_app_info import WebAppInfo

BOT_TOKEN = '6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kb_builder = ReplyKeyboardBuilder()

contact_btn = KeyboardButton(
    text='Отправить телефон',
    request_contact=True
)
geo_btn = KeyboardButton(
    text='Отправить геолокацию',
    request_location=True
)
poll_btn = KeyboardButton(
    text='Создать опрос',
    request_poll=KeyboardButtonPollType(type='regular')
)
quiz_btn = KeyboardButton(
    text='Создать викторину',
    request_poll=KeyboardButtonPollType(type='quiz')
)
web_btn = KeyboardButton(
    text='Start Web App',
    web_app=WebAppInfo(url='https://stepik.org/')
)

kb_builder.row(contact_btn, geo_btn, poll_btn, quiz_btn, web_btn, width=1)

keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Эксперименты со специальными кнопками',
        reply_markup=keyboard
    )

if __name__ == '__main__':
    dp.run_polling(bot)