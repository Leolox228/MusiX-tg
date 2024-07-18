# chart.py
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid

async def send_chart(callback_query: types.CallbackQuery, bot: Bot, client):
    await bot.answer_callback_query(callback_query.id)
    page = int(callback_query.data.split('_')[1]) if '_' in callback_query.data else 1
    chart = client.chart()
    tracks = chart.chart.tracks
    total_pages = (len(tracks) + 19) // 20

    start_index = (page - 1) * 20
    end_index = start_index + 20
    tracks_on_page = tracks[start_index:end_index]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔥 Чарт 🔥", callback_data=str(uuid.uuid4()))]])
    for i, track in enumerate(tracks_on_page, start_index + 1):
        track_info = track.track
        artist_names = ', '.join([artist.name for artist in track_info.artists])
        i1 = i
        if i == 1:
            i1 = '🏆'
        elif i == 2:
            i1 = '🥈'
        elif i == 3:
            i1 = '🥉'
        button_text = f"{i1}. {track_info.title} - {artist_names}"
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=button_text, switch_inline_query_current_chat=f"/dbi {track_info.id}")])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="<", callback_data=f"chart_{page - 1}"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="chart_page"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text=">", callback_data=f"chart_{page + 1}"))
    keyboard.inline_keyboard.append(navigation_buttons)

    refresh_button = [InlineKeyboardButton(text="Обновить чарт! 🔥", callback_data=f"chartrefresh_{page}")]
    keyboard.inline_keyboard.append(refresh_button)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Треки, популярные на Яндекс Музыке прямо сейчас",
        reply_markup=keyboard
    )
