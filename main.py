import asyncio
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultAudio, ChosenInlineResult
from yandex_music import Client
from dotenv import load_dotenv
from inline_handlers import empty_query_handler, dbi_handler, info_handler, start_handler, search_tracks_handler, text_handler
from chart import send_chart
import os

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
YA_MUSIC_API_KEY = os.getenv('YA_MUSIC_API_KEY')
PAGE_SIZE = 20
client = Client(YA_MUSIC_API_KEY).init()
bot = Bot(TELEGRAM_API_KEY)
dp = Dispatcher()

async def find_tracks(track_name):
    try:
        search_result = client.search(track_name, type_='track')
        
        if search_result.tracks and search_result.tracks.results:
            tracks = search_result.tracks.results
            return tracks
        else:
            print(f"No tracks found for '{track_name}'")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

async def find_track_by_id(track_id):
    tracks = client.tracks(track_id)
    return tracks[0]

@dp.message(lambda message: message.text.startswith('/start'))
async def handle_message(message: types.Message):
    user_first_name = message.from_user.first_name
    reply_text = f"Привет, {user_first_name}! Бот работает и в inline режиме!"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Запустить 🚀",
                            switch_inline_query_current_chat="/start"
                        ),
                        InlineKeyboardButton(
                            text="Чарт 🔥",
                            callback_data="chart"
                        )
                    ]
            ])
    await message.reply(reply_text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('chart'))
async def chart_handler(callback_query: types.CallbackQuery):
    await send_chart(callback_query, bot, client)
    
@dp.callback_query(lambda c: c.data.startswith('chartrefresh'))
async def refresh_chart(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await chart_handler(callback_query)

@dp.inline_query()
async def inline_query_handler(query: types.InlineQuery):
    query_text = query.query.strip()
    if query_text == "":
        await empty_query_handler(query)
    elif query_text.startswith("/dbi "):
        track_id = query_text.split()[1]
        await dbi_handler(query, track_id, find_track_by_id)
    elif query_text.startswith("/text "):
        track_id = query_text.split()[1]
        lyrics = client.tracks_lyrics(track_id, "TEXT").fetch_lyrics()
        await text_handler(query, lyrics, track_id, find_track_by_id)
    elif query_text.startswith("/info "):
        track_id = query_text.split()[1]
        try:
            lyrics = client.tracks_lyrics(track_id, "TEXT").fetch_lyrics()
            await info_handler(query, track_id, find_track_by_id, lyrics)
        except Exception as e:
            print(e)
            await info_handler(query, track_id, find_track_by_id, None)
    elif query_text.startswith("/start"):
        await start_handler(query)
    else:
        await search_tracks_handler(query, find_tracks)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
