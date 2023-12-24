from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher()

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Способы связи'),
        BotCommand(command='/payment',
                   description='Платежи')
    ]

    await bot.set_my_commands(main_menu_commands)

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)