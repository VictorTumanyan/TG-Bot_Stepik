from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart

from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher()

big_button1 = InlineKeyboardButton(
    text='Большая кнопка 1',
    callback_data='big_button1_pressed'
)

big_button2 = InlineKeyboardButton(
    text='Большая кнопка 2',
    callback_data='big_button2_pressed'
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[big_button1],
                     [big_button2]]
)

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Это инлайн-кнопки с параметром "callback"',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == 'big_button1_pressed')
async def process_button1_pressed(callback: CallbackQuery):
    if callback.message.text != 'Была нажата кнопка "Большая кнопка 1"':
        await callback.message.edit_text(
            text='Была нажата кнопка "Большая кнопка 1"',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()

@dp.callback_query(F.data == 'big_button2_pressed')
async def process_button2_pressed(callback: CallbackQuery):
    if callback.message.text != 'Была нажата кнопка "Большая кнопка 2"':
        await callback.message.edit_text(
            text='Была нажата кнопка "Большая кнопка 2"',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()

if __name__ == '__main__':
    dp.run_polling(bot)