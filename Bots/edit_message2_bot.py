from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
                           InputMediaAudio, InputMediaPhoto, InputMediaDocument, InputMediaVideo)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher()

LEXICON: dict[str, str] = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'video': '🎬 Видео',
    'document': '📑 Документ',
    'voice': '📢 Голосовое сообщение',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': 'AgACAgIAAxkBAAIFDmWssODy7PpF6Qb1lHuZMQO_K67hAAJ12jEbgRVpSQ_KRCnMGUAUAQADAgADcwADNAQ',
    'photo_id2': 'AgACAgIAAxkBAAIFEGWssO3f8Whct-4Cecry5bggYRrtAAJ52jEbgRVpSaaGbV4Q-1KjAQADAgADcwADNAQ',
    'voice_id1': 'AwACAgIAAxkBAAIFFGWssVsZyRRxMa3lssI1vymfWUEzAAKmPwACgRVpSWQWjvPAD4J6NAQ',
    'voice_id2': 'AwACAgIAAxkBAAIFFmWssWKgO2SoKBeuq2zDE9XdvHPjAAKnPwACgRVpSX6aHBbQIKYbNAQ',
    'document_id1': 'BQACAgIAAxkBAAIFMmWsspFmJKMJWeXNqdK5I1DTZ75DAAIvNgACcewBSpUOcUObhpT5NAQ',
    'document_id2': 'BQACAgQAAxkBAAIFM2WsspqDMQABjgZWnOPQZCu-jaeB2QACiREAAqpNEVPGTnvkasWblDQE',
    'video_id1': 'BAACAgIAAxkBAAIFKmWsskSTqthPKbzZqf108q_VEfukAAKtPwACgRVpSSZd58g7F2bcNAQ',
    'video_id2': 'BAACAgIAAxkBAAIFLGWsskxB0_DT_h1jdsrb33tIKRUIAAKuPwACgRVpSafBKXkP_vDkNAQ',
}

def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs:
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()

@dp.message(CommandStart())
async def process_start_command(message: Message):
    markup = get_markup(2, 'video')
    await message.answer_document(
        document=LEXICON['video_id1'],
        caption='Это видео 1',
        reply_markup=markup
    )

@dp.callback_query(F.data.in_(
    ['text', 'video', 'document', 'photo', 'voice']
))
async def process_button_press(callback: CallbackQuery, bot: Bot):
    try:
        markup = get_markup(2, 'photo')
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=LEXICON['photo_id2'],
                caption='Это фото 2'
            ),
            reply_markup=markup
        )
    except TelegramBadRequest:
        markup = get_markup(1, 'video')
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaVideo(
                media=LEXICON['video_id1'],
                caption='Это видео 1'
            ),
            reply_markup=markup
        )

@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Не понимаю')

if __name__ == '__main__':
    dp.run_polling(bot)