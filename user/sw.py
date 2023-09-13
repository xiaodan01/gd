from telethon import events
from .login import user

from .. import jdbot
from jbot import chat_id, jdbot, logger
from ..bot.utils import logger, AUTH_FILE, QL, get_cks
from asyncio import sleep
from urllib.parse import unquote
import os
import re
import time
import traceback


@user.on(events.NewMessage(pattern=r'^sw', outgoing=True))
async def showlist(event):
    try:
        if QL:
            ckfile = AUTH_FILE
        else:
            ckfile = CONFIG_SH_FILE
        cookies = get_cks(ckfile)
        
        if re.search('\d{1,2}', event.raw_text) and (len(event.raw_text.split(' ')[1]) == 1 or len(event.raw_text.split(' ')[1]) == 2):
            i = int(event.raw_text.split(' ')[1])
            ck = cookies[i-1]
            ptpin=ck.split("pt_pin=")[1].split(";")[0]
            if re.search('%', ptpin):
                ptpin = unquote(ptpin, 'utf-8')
        
        strreturn=""
        with open("/ql/data/scripts/gifts.csv",'r',encoding='utf-8') as fr:
            #for item in fr:
            #iteminfo=item.split(",")
            if event.raw_text == "sw":
                listtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                strreturn+="日期:"+listtime+"\n"
                for item in fr:
                    iteminfo=item.split(",")
                    if listtime==iteminfo[0][0:10]:
                        if strreturn!="":
                            strreturn+="\n" 
                        strreturn+=iteminfo[0][11:19]+'   '+iteminfo[1]
            if re.search('\d{1,2}', event.raw_text) and (len(event.raw_text.split(' ')[1]) == 1 or len(event.raw_text.split(' ')[1]) == 2):
                for item in fr:
                    iteminfo=item.split(",")
                    if ptpin==iteminfo[2]:
                        if strreturn!="":
                            strreturn+="\n" 
                        strreturn+=iteminfo[0][0:19]+'   '+iteminfo[1]
            if re.search('\d{4}[-/]?\d{2}[-/]?\d{2}', event.raw_text):
                listtime = event.raw_text.split(' ')[1]
                strreturn+="日期:"+listtime+"\n"
                for item in fr:
                    iteminfo=item.split(",")
                    if listtime==iteminfo[0][0:10]:
                        if strreturn!="":
                            strreturn+="\n" 
                        strreturn+=iteminfo[0][11:19]+'   '+iteminfo[1]
            if re.search('[\u4e00-\u9fa5]', event.raw_text):
                name = event.raw_text.split(' ')[1]
                for item in fr:
                    iteminfo=item.split(",")
                    if re.search(f'{name}', iteminfo[1]):
                        if strreturn!="":
                            strreturn+="\n" 
                        strreturn+=iteminfo[0][0:19]+'   '+iteminfo[1]
                    
            itemlist=strreturn.split("\n")
            if len(itemlist)>30:
                if re.search('\d{1,2}', event.raw_text) and (len(event.raw_text.split(' ')[1]) == 1 or len(event.raw_text.split(' ')[1]) == 2):
                    strreturn="查询到账号"+ptpin+"最近15条奖品记录:\n"
                else:
                    strreturn="查询到最近15条奖品记录:\n"
                for num in range(len(itemlist)-30,len(itemlist)):
                    if strreturn!="":
                        strreturn+="\n"
                    strreturn+=itemlist[num]
            else:
                if re.search('\d{1,2}', event.raw_text) and (len(event.raw_text.split(' ')[1]) == 1 or len(event.raw_text.split(' ')[1]) == 2):
                    strreturn="查询到账号"+ptpin+"的奖品信息:\n\n"+strreturn
                if re.search('[\u4e00-\u9fa5]', event.raw_text):
                    name = event.raw_text.split(' ')[1]
                    strreturn="查询关键字-"+name+"-的奖品信息:\n\n"+strreturn
                else:
                    strreturn="查询到奖品信息:\n"+strreturn
                    
            if strreturn!="":
                await event.edit(strreturn)
                await sleep(25)
                await event.delete()
            else:
                await event.edit("没有找到奖品列表，继续加油吧!")
                await sleep(25)
                await event.delete()
            
    except Exception as e:
        title = ""
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(
            chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")