import time
import os
import requests
import asyncio
from typing import Union
from wechaty import (
    Contact,
    Message,
    Wechaty,
    Room,
)

os.environ['WECHATY_PUPPET']= 'wechaty-puppet-hostie'
os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = 'puppet_donut_25e31edab29faf7d'
url = r'https://sc.ftqq.com/SCU108142Te3389e6c15b3491545b65780e559503d5f27661e050c0.send?text={}&desp={}'

def get_time():
    return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))

async def on_message(msg: Message):
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    if text == '#ding':
        conversation: Union[
            Room, Contact] = from_contact if room is None else room
        await conversation.ready()
        await conversation.say('dong')
        if room and room.payload.topic in ['ChatOps - Donut', '量化动态播报']:
            target_friend = bot.Contact.load('wzhwno1')
            print(target_friend)
            await target_friend.say('[{}]: Success replied at {}'.format(get_time(), room.payload.topic))

async def on_logout():
    text = 'Wechat abnormal logout!'
    desp = '[{}]: Abnormal logout, pls re-login asap.'.format(get_time())
    requests.get(url.format(text, desp))

async def on_error():
    text = 'Wechaty error!'
    desp = '[{}]: Wechaty error, pls check.'.format(get_time())
    requests.get(url.format(text, desp))

async def on_room_join(room, inviteeList, inviter):
    print(room, inviteeList, inviter)
    if room.payload.topic in ['ChatOps - Donut', '量化动态播报']:
        conversation: Union[Room, Contact] = room
        await conversation.ready()
        await conversation.say('欢迎{}进群，感谢{}的邀请!'.format(str(inviteeList), inviter))
        target_friend = bot.Contact.load('wzhwno1')
        await target_friend.say('Success replied at {}'.format(get_time()))

async def main():
    global bot
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print('Scan QR Code to login: {}\nhttps://wechaty.github.io/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logined'.format(user)))
    bot.on('message', on_message)
    bot.on('room-join', on_room_join)
    bot.on('logout', on_logout)
    bot.on('error', on_error)
    await bot.start()

asyncio.run(main())
