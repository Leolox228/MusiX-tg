# inline_handlers.py
import uuid
from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultAudio, InlineKeyboardMarkup, InlineKeyboardButton

async def empty_query_handler(query: types.InlineQuery):
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Кажется вы ничего не ввели",
            description="Введите запрос",
            input_message_content=InputTextMessageContent(
                message_text="Кажется, вы ошиблись (точнее ваш собеседник)"
            ),
            thumb_url="https://eu-central.storage.cloudconvert.com/tasks/8c49f839-3041-49b3-a6e6-7beacbb40e7c/zloi-smail-1%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20240711%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20240711T204723Z&X-Amz-Expires=86400&X-Amz-Signature=589cfc232afa4d7e025ea4bd5c51a4813349704c60faa270b3cf1971af930fdc&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3D%22zloi-smail-1%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject",
        )
    ]
    await query.answer(results, cache_time=300)

async def dbi_handler(query: types.InlineQuery, track_id: str, find_track_by_id):
    track = await find_track_by_id(track_id)
    artist_names = ', '.join([artist.name for artist in track.artists])
    download_info_list = track.get_download_info()
    best_download_info = list(filter(lambda x: x.codec == "mp3", download_info_list))
    best_download_info = max(download_info_list, key=lambda x: int(x.bitrate_in_kbps))
    audio_url = best_download_info.get_direct_link()
    results = [
        InlineQueryResultAudio(
            id=str(uuid.uuid4()),
            audio_url=audio_url,
            title=track.title,
            performer=artist_names,
            thumb_url=track.cover_uri.replace("%%", "200x200"),
            duration=track.duration_ms // 1000,
        )
    ]
    await query.answer(results, cache_time=300)

async def info_handler(query: types.InlineQuery, track_id: str, find_track_by_id, lyrics):
    track = await find_track_by_id(track_id)
    artist_names = ', '.join([artist.name for artist in track.artists])
    album = track.albums[0].title
    genre = track.albums[0].genre
    year = track.albums[0].year
    if lyrics != None:
        text = f"{track.title} - {artist_names}\nАльбом: {album}\nЖанр: {genre}\nГод выпуска: {year}"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Текст",
                    switch_inline_query_current_chat=f"/text {track.id}"
                ),
            ]
        ])
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=track.title,
                description=artist_names,
                input_message_content=InputTextMessageContent(
                    message_text=text,
                    parse_mode="Markdown"
                ),
                thumbnail_url=track.cover_uri.replace("%%", "200x200"),
                reply_markup=keyboard
            )
        ]
    else:
        text = f"{track.title} - {artist_names}\nАльбом: {album}\nЖанр: {genre}\nГод выпуска: {year}"
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=track.title,
                description=artist_names,
                input_message_content=InputTextMessageContent(
                    message_text=text,
                    parse_mode="Markdown"
                ),
                thumbnail_url=track.cover_uri.replace("%%", "200x200")
            )
        ]
    await query.answer(results, cache_time=300)

async def start_handler(query: types.InlineQuery):
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Введи название трека вместо /start",
            description="Начни пользоваться ботом!",
            input_message_content=InputTextMessageContent(
                message_text="Кажется, вы ошиблись (точнее ваш собеседник)"
            ),
            thumb_url="https://s1033sas.storage.yandex.net/rdisk/886e9b1d6503a89b5e6e8b9170c1d6f995dd529c8104c8aed46914b04909f916/6691c548/2YOKrglluBTIJ-pkGmpR9TgbQK1VPGGZDguvPAAGhbrtj2DNrfdk-5gVgOuEJDT9UunjjIhfGIGRdcu024Tzlg==?uid=1664472674&filename=photo_2024-07-12_23-07-22.jpg&disposition=attachment&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=1664472674&fsize=19025&hid=41414f9f282819eabb7abd93bd116ab9&media_type=image&tknv=v2&etag=4487573f34372ee2c25bd77940a39c91&ts=61d15c885e200&s=a612eb23035acfe078dbe3a8eb0e2505d0cd323ef2a7e9f60a15b9fb30c04516&pb=U2FsdGVkX1-WgBOa31T1ehmkT94C6eu5PshxFYukA1sDYwotGGAOqXYhYr84DKwrtNku7pIKBd-1C5eU-mQJ2f0e20wblZVn8dyHB33x_KY"
        )
    ]
    await query.answer(results, cache_time=300)

async def text_handler(query: types.InlineQuery, lyrics, track_id: str, find_track_by_id):
    track = await find_track_by_id(track_id)
    artist_names = ', '.join([artist.name for artist in track.artists])
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=track.title,
            description=artist_names,
            input_message_content=InputTextMessageContent(
                message_text=f"{track.title} - {artist_names}\n\n`{lyrics}`",
                parse_mode="Markdown"
            ),
            thumb_url=track.cover_uri.replace("%%", "200x200")
        )
    ]
    await query.answer(results, cache_time=300)

async def search_tracks_handler(query: types.InlineQuery, find_tracks):
    tracks = await find_tracks(query.query)
    results = []
    if len(tracks) == 0:
        results.append(InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Ничего не найдено",
            description="Попробуйте ещё раз",
            input_message_content=InputTextMessageContent(
                message_text="Кажется, вы ошиблись (точнее ваш собеседник)"
            ),
            thumb_url="https://papik.pro/uploads/posts/2022-08/1661967607_2-papik-pro-p-smailik-neponimaniya-png-2.png",
        ))
    for track in tracks[:12]:
        artist_names = ', '.join([artist.name for artist in track.artists])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎵 Скачать",
                    switch_inline_query_current_chat=f"/dbi {track.id}"
                ),
                InlineKeyboardButton(
                    text="📄 Инфо",
                    switch_inline_query_current_chat=f"/info {track.id}"
                ),
            ]
        ])
        try:
            results.append(InlineQueryResultArticle(
                id=str(track.id),
                title=track.title,
                description=artist_names,
                input_message_content=InputTextMessageContent(
                    message_text=f"{track.title} - {artist_names}"
                ),
                thumb_url=track.cover_uri.replace("%%", "100x100"),
                reply_markup=keyboard
            ))
        except Exception as e:
            print(f"An error occurred: {e}")

    await query.answer(results, cache_time=300)
