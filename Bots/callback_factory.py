from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (CallbackQuery, Message,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher()

class GoodsCallbackFactory(CallbackData, prefix='goods'):
    category_id: int
    subcategory_id: int
    item_id: int

# my_callback_data_1 = GoodsCallbackFactory(
#     category_id=2,
#     subcategory_id=0,
#     item_id=0
# )

# print(my_callback_data_1.pack())

# button_1 = InlineKeyboardButton(
#     text='Категория 1',
#     callback_data=GoodsCallbackFactory(
#         category_id=1,
#         subcategory_id=0,
#         item_id=0
#     ).pack()
# )

# button_2 = InlineKeyboardButton(
#     text='Категория 2',
#     callback_data=GoodsCallbackFactory(
#         category_id=2,
#         subcategory_id=0,
#         item_id=0
#     ).pack()
# )

# markup = InlineKeyboardMarkup(
#     inline_keyboard=[[button_1], [button_2]]
# )

# Инициализируем билдер инлайн-клавиатуры
builder = InlineKeyboardBuilder()

# В БИЛДЕР МОЖНО ДОБАВЛЯТЬ БЕЗ МЕТОДА .pack()
# Добавляем первую кнопку в билдер
builder.button(
    text='Категория 1',
    callback_data=GoodsCallbackFactory(
        category_id=1,
        subcategory_id=0,
        item_id=0
    )
)

# Добавляем вторую кнопку в билдер
builder.button(
    text='Категория 2',
    callback_data=GoodsCallbackFactory(
        category_id=2,
        subcategory_id=0,
        item_id=0
    )
)

# Сообщаем билдеру схему размещения кнопок (здесь по одной в ряду)
builder.adjust(1)

# Этот хэндлер будет срабатывать на команду /start
# и отправлять пользователю сообщение с клавиатурой
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Вот такая клавиатура',
        reply_markup=builder.as_markup()
    )

# @dp.message(CommandStart())
# async def process_start_command(message: Message):
#     await message.answer(
#         text='Вот такая клава',
#         reply_markup=markup
#     )

@dp.callback_query(GoodsCallbackFactory.filter())
async def process_category_press(callback: CallbackData,
                                 callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())
    await callback.answer()

@dp.callback_query()
async def process_any_inline_button_press(callback: CallbackQuery):
    print(callback.model_dump_json(indent=4, exclude_none=True))

if __name__ == '__main__':
    dp.run_polling(bot)