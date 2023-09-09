import os
import re
import sys
import time
import traceback

import asyncio
import paramiko
import requests
from telethon import events
from .. import user, chat_id, jdbot, logger
#, TOKEN 
#1.apk add --no-cache gcc g++ python3-dev py-pip mysql-dev linux-headers libffi-dev openssl-dev
#2.pip3 install pycrypto
#3.pip install --upgrade pip
#4.依赖面板py里安装wheel
#5.py里安装paramiko

#bot_id = int(TOKEN.split(':')[0])
bot_id = "5614343782"
from cacheout import FIFOCache

cache = FIFOCache(maxsize=10)
cache2 = FIFOCache(maxsize=10)
ssh = paramiko.SSHuser()
know_host = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(know_host)

hostname = "192.168.1.2"
username = "root"
password = "****"
port = 22
ip_command = "curl cip.cc"
restart_command = "/sbin/ifup wan"

@user.on(events.NewMessage(chats=bot_id, pattern=r'[^_-].*'))
async def listen_and_changeip(context):
    try:
        if context.sender_id != bot_id:
            return
        text = context.text
        if not re.search(r'IP 493 493 493|IP 403 403 403',text):
            return
        ssh.connect(hostname=hostname,port=port,username=username,password=password)
        stdin, stdout, stderr = ssh.exec_command(ip_command)
        ip_origin = stdout.read().decode()
        await jdbot.send_message(chat_id, f'变更前 {ip_origin}')
        for i in range(2):
            ssh.exec_command(restart_command)
            await asyncio.sleep(10)
            stdin, stdout, stderr = ssh.exec_command(ip_command)
            ip_changed = stdout.read().decode()
            if ip_changed=='':
                await jdbot.send_message(chat_id, f"未获取到IP，等待2s再次获取")
                await asyncio.sleep(2)
            stdin, stdout, stderr = ssh.exec_command(ip_command)
            ip_changed = stdout.read().decode()
            info =f'变更后 {ip_changed}'
            if ip_changed!=ip_origin and ip_changed!='':
                break
            else:
                await jdbot.send_message(chat_id, f"IP未变更，第{i+2}次重拨中>>>")
            info = f'IP未变更，请手动重拨'
        await jdbot.send_message(chat_id, f'{info}')
        ssh.close()
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
        
        
@user.on(events.NewMessage(chats=bot_id, pattern='^重拨'))
async def router(event):
    try:
        logger.info("监控到重拨指令，开始执行")
        ssh.connect(hostname=hostname,port=port,username=username,password=password)
        stdin, stdout, stderr = ssh.exec_command(ip_command)
        ip_origin = stdout.read().decode()
        await event.edit(f'变更前 {ip_origin}')
        start = time.time()
            
        for i in range(2):
            ssh.exec_command(restart_command)
            await asyncio.sleep(3)
            stdin, stdout, stderr = ssh.exec_command(ip_command)
            ip_changed = stdout.read().decode()
            if ip_changed=='':
                for j in range(15):
                    await asyncio.sleep(1)
                    stdin, stdout, stderr = ssh.exec_command(ip_command)
                    ip_changed = stdout.read().decode()
                    if ip_changed!='':
                        break
            info =f'变更后 {ip_changed}'
            if ip_changed!=ip_origin and ip_changed!='':
                break
            else:
                await jdbot.send_message(event.chat_id, f"IP未变更，第{i+2}次重拨中>>>")
            info = f'IP未变更，请手动重拨'
        end = time.time()
        exetime = (end - start)
        exetime = ("%.2f" % exetime)
        await jdbot.send_message(chat_id, f'用时{exetime}秒，已超越99.9%群友\n\n{info}')
        ssh.close()
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")

# 设置变量
@user.on(events.NewMessage(chats=bot_id, pattern='^ip'))
async def ip(event):
    try:
        logger.info("监控到ip指令，开始执行")
        ssh.connect(hostname=hostname,port=port,username=username,password=password)
        stdin, stdout, stderr = ssh.exec_command(ip_command)
        ip1 = stdout.read().decode()
        await jdbot.send_message(chat_id, f'当前 {ip1}')
        ssh.close()

    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
