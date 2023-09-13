#!/usr/bin/env python3
# Author : Annyooo
# Data   : 2022-02-18


import time, sys, os, re, traceback, asyncio
from .. import user, chat_id, jdbot, logger, TOKEN
from telethon import events

bot_id = int(TOKEN.split(':')[0])


@user.on(events.NewMessage(chats=bot_id, pattern=r"^shop$"))
async def shopGift(event):
    try:
        info = f'/cmd task jd_task_shopGift.js now'
        msg = await user.send_message(bot_id, info)
        await user.delete_messages(bot_id, msg)
    except Exception as e:
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        logger.error(f"错误--->{function}\n{str(e)}\n{details}\n{traceback.format_exc()}")


@user.on(events.NewMessage(chats=bot_id, pattern=r"^hb$"))
async def assets(event):
    try:
        info = f'/cmd task jd_task_assets.js now'
        msg = await user.send_message(bot_id, info)
        await user.delete_messages(bot_id, msg)
    except Exception as e:
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        logger.error(f"错误--->{function}\n{str(e)}\n{details}\n{traceback.format_exc()}")

@user.on(events.NewMessage(chats=bot_id, pattern=r"^rm$"))
async def assets(event):
    try:
        info = f'/cmd task KingRan_KR/jd_cleancart_nolan.js desi JD_COOKIE 1-4'
        msg = await user.send_message(bot_id, info)
        await user.delete_messages(bot_id, msg)
    except Exception as e:
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        logger.error(f"错误--->{function}\n{str(e)}\n{details}\n{traceback.format_exc()}")

@user.on(events.NewMessage(chats=bot_id, pattern=r"^magic$"))
async def assets(event):
    try:
        info = f'/cmd pm2 restart magic'
        msg = await user.send_message(bot_id, info)
        await user.delete_messages(bot_id, msg)
    except Exception as e:
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        logger.error(f"错误--->{function}\n{str(e)}\n{details}\n{traceback.format_exc()}")