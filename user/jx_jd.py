from telethon import events
from .. import user, jdbot, chat_id, TOKEN
import re
import requests
import asyncio


bot_id = int(TOKEN.split(':')[0])

@user.on(events.NewMessage(pattern=r'^(jx)$', outgoing=True))
async def jcmd(event):
    reply = await event.get_reply_message()
    chat = await event.get_chat()
    theuser = jdbot if chat.id == bot_id else user
    toid = chat_id if chat.id == bot_id else chat.id
    if reply:
        msg_text = reply.text

        url = 'http://192.168.1.2:3001/JComExchange'
        payload = {'ck':reply}
        data = requests.post(url,data=payload).json()

        code = data['code']
        if code == '0':
            data = data["data"]
            msg = f'【活动信息】: {data["title"]}\n【口令发起人】：{data["userName"]}\n【活动链接】: {data["jumpUrl"]}'
            await theuser.send_message(toid,msg)