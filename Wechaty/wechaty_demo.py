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

async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    if msg.text() == 'ding':
        await msg.say('dong')
    elif text == '#ding':
        conversation: Union[
            Room, Contact] = from_contact if room is None else room
        await conversation.ready()
        await conversation.say('dong')
        if room.payload.topic == 'ChatOps - Donut':
            url = r'https://sc.ftqq.com/SCU108142Te3389e6c15b3491545b65780e559503d5f27661e050c0.send?text={}&desp={}'
            text = 'New pingpong coming'
            desp = 'Success replied at {}'.format(time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time())))
            requests.get(url.format(text, desp))

async def main():
    global bot
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print('Scan QR Code to login: {}\nhttps://wechaty.github.io/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logined'.format(user)))
    bot.on('message', on_message)
    await bot.start()

asyncio.run(main())
