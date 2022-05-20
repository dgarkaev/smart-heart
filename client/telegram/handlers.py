from aiogram import types
from aiogram.types import InputMediaDocument, ChatActions, ContentType
import asyncio
from load_all import redis, logging, bot, dp
import json
import os
import aioschedule
from config import APP_NAME, ADMIN_ID


@dp.message_handler(commands=['start'])
async def handler_welcome(message: types.Message):
    await message.answer(f"User ID: {message.from_user.id}")
    txt = f"""start user:
id: {message.from_user.id}
full_name: {message.from_user.full_name}
username: {message.from_user.username}
mention: {message.from_user.mention}
date: {message.date}""".strip()
    await dp.bot.send_message(ADMIN_ID, txt)


@dp.message_handler(commands=['help'])
async def handler_help(message: types.Message):
    await message.answer("Instructions:\nTODO")


@dp.message_handler(content_types=[ContentType.AUDIO, ContentType.VOICE, ContentType.DOCUMENT])
async def handler_audio(message: types.Message):
    if message.voice:
        content = message.voice
    if message.audio:
        content = message.audio
    if message.document:
        content = message.document

    path_base = os.path.dirname(os.path.abspath(__file__))
    path_base = os.path.dirname(os.path.dirname(path_base))
    path_base = os.path.join(path_base, 'pcg')

    user_id = message.from_user.id
    file_id = content.file_id
    file_info = await bot.get_file(file_id)
    file_name = os.path.basename(file_info.file_path)
    file_path = os.path.join(path_base, f'{user_id}', file_name)
    rz = await bot.download_file_by_id(file_id, destination=file_path)
    task = {
        'id': 'pcg',
        'type': 'file',
        'user_id': user_id,
        'value': file_path
    }
    tn = await redis.rpush(f'{APP_NAME}:task', json.dumps(task))
    # отправить сообщение пользователю
    await redis.rpush(f'{APP_NAME}:cmd', json.dumps({'user_id': user_id, 'type': 'text', 'value': f'The file is queued:[{tn}] for processing.'}))


async def wait_query():
    " Обработка команд из очереди "
    while True:
        rz = await redis.lpop(f'{APP_NAME}:cmd')
        if rz is None:
            await asyncio.sleep(1)
            # print('rz is None')
            continue

        # обработка команды
        try:
            cmd = json.loads(rz)
            user_id = int(cmd['user_id'])
            t = cmd['type']

            if t == 'text':
                await bot.send_message(chat_id=user_id, text=cmd['value'])
                continue

            if t == 'document':
                await bot.send_chat_action(chat_id=user_id, action=ChatActions.UPLOAD_DOCUMENT)
                await bot.send_document(chat_id=user_id, document=open(cmd['value'], 'rb'))
                continue

            if t == 'photo':
                await bot.send_chat_action(chat_id=user_id, action=ChatActions.UPLOAD_PHOTO)
                await bot.send_photo(chat_id=user_id, photo=open(cmd['value'], 'rb'))
                continue

        except Exception as e:
            # print(e)
            pass


async def scheduler():
    aioschedule.every(1).minutes.do(job1m)
    while 1:
        await aioschedule.run_pending() #run_all()
        await asyncio.sleep(1)

async def job1m():
    # TODO
    ...