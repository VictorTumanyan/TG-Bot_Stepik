import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

BOT_TOKEN = '6737278711:AAEd7eFofaoj5n5n69lqBvb71RrghrS-xkE'
ATTEMPTS = 5
IN_GAME_TEXT = 'Сейчас мы играем, поэтому ты можешь либо отправить число, либо отменить игру командой /cancel'
USER_PATTERN = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}

users = {}
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_random_number() -> int:
    return random.randint(1, 100)

@dp.message(CommandStart())
async def process_start_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users.keys():
        users[user_id] = {'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }
    users[user_id]['in_game'] = False
    users[user_id]['total_games'] = 0
    users[user_id]['wins'] = 0
    await message.answer(text =
        f'Здарова, заебал!\n'
        f'Давай с тобой сыграем в игру "Угадай число"?\n\n'
        f'P.s. если хочешь узнать правила игры, отправь команду /help :)'
    )

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=
        f'Итак, игра заключается в том, что я загадываю любое число от 1 до 100, а тебе нужно его отгадать.\n'
        f'Количество попыток: {ATTEMPTS}.\n'
        f'Если число не угадано, то я сообщу, больше или меньше загаданное число относительно названного тобой.\n'
        f'Если хочешь выйти из игры, то можешь воспользоваться командой /cancel.\n\n'
        f'Также вот список команд, которые ты можешь использовать, общаясь со мной:\n\n'
        f'Используются НЕ во время игры:\n'
        f'\t/start - запускает бота заново, все сохранения удаляются;\n'
        f'\t/help - показывает правила игры;\n'
        f'\t/stat - показывает статистику, сколько раз у тебя получалось угадать число;\n\n'
        f'Используются во время игры:\n'
        f'\t/cancel - отменяет игру.'
    )

@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    user_id = message.from_user.id
    await message.answer(text=
        f"Количество побед: {users[user_id]['wins']}\n"
        f"Количество сыгранных игр: {users[user_id]['total_games']}\n"
        f"Попробуешь ещё ?)"
    )

@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    user_id = message.from_user.id
    if users[user_id]['in_game']:
        users[user_id]['in_game'] = False
        await message.answer(text=
            f'Игра отменена\n'
            f'Если захочешь поиграть, то отправь слово "Игра"\n'
            f'Не теряйся :*'
        )
    else:
        await message.answer(text=
            f'Так мы ещё и не играем\n'
            f'Может, тогда начнём ?)'
        )

@dp.message(F.text.lower().in_(['да', 'давай', 'погнали', 'хочу играть', 'го', 'игра', 'сыграть', 'поехали']))
async def want_play(message: Message):
    user_id = message.from_user.id
    if users[user_id]['in_game']:
        await message.answer(text=IN_GAME_TEXT)
    else:
        users[user_id]['in_game'] = True
        users[user_id]['secret_number'] = get_random_number()
        users[user_id]['attempts'] = ATTEMPTS
        await message.answer(text=
            f'Заебумба!\n'
            f'Давай угадывай'
        )


@dp.message(F.text.lower().in_(['нет', 'не хочу', 'не', 'не буду', 'пошёл ты']))
async def not_want_play(message: Message):
    user_id = message.from_user.id
    if users[user_id]['in_game']:
        await message.answer(text=IN_GAME_TEXT)
    else:
        await message.answer(text=
            f'Жаль, брат :(\n'
            f'Если захочешь поиграть, то отправь слово "Игра"'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and (1 <= int(x.text) <= 100))
async def send_number(message: Message):
    user_id = message.from_user.id
    if users[user_id]['in_game']:
        input_num = int(message.text)
        if input_num == users[user_id]['secret_number']:
            users[user_id]['in_game'] = False
            users[user_id]['total_games'] += 1
            users[user_id]['wins'] += 1
            await message.answer(text=
                f'Ну красавчик, угадал\n'
                f'Сыграем ещё?'
            )
        elif input_num < users[user_id]['secret_number']:
            users[user_id]['attempts'] -= 1
            await message.answer(text='Больше')
        else:
            users[user_id]['attempts'] -= 1
            await message.answer(text='Меньше')

        if users[user_id]['attempts'] == 0:
            users[user_id]['in_game'] = False
            users[user_id]['total_games'] += 1
            await message.answer(text=
                f'Ну всё, бро, ты доигрался :(\n'
                f'Загаданное число: {users[user_id]["secret_number"]}\n'
                f'Давай ещё сыграем?'
            )
    else:
        await message.answer(text=
            f'Ииияяяя\n'
            f'Давай сначала напиши слово "Погнали", потом уже будешь угадывать, эли'
        )

@dp.message()
async def any_message(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(text=IN_GAME_TEXT)
    else:
        await message.answer(text=
            f'Я не знаю, как реагировать на твоё сообщение.\n'
            f'Попробуй почитать правила, отправив команду /help или сразу начни играть, отправив слово "Поехали"'
        )


if __name__ == "__main__":
    dp.run_polling(bot)