# from typing import Any
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import BaseFilter

BOT_TOKEN = '6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# admin_ids: list[int] = [6325704944]

# class IsAdmin(BaseFilter):
#     def __init__(self, admin_ids: list[int]) -> None:
#         self.admin_ids = admin_ids

#     async def __call__(self, message: Message) -> bool:
#         return message.from_user.id in self.admin_ids

# @dp.message(IsAdmin(admin_ids))
# async def answer_if_admins_update(message: Message):
#     await message.answer(text='Вы админ')

# @dp.message()
# async def answer_if_not_admins_update(message: Message):
#     await message.answer(text='Вы не админ')

class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        if numbers:
            return {'nums': numbers}
        return False

@dp.message(F.text.lower().startswith('найди числа'), NumbersInMessage())
async def process_if_numbers(message: Message, nums: list[int]):
    await message.answer(text=f'Нашёл: {", ".join(str(num) for num in nums)}')

@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(text='Ничего не нашёл :(')

if __name__ == '__main__':
    dp.run_polling(bot)