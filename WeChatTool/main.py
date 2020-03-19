# -*-coding=utf8-*-
import itchat
from itchat.content import *
from logger import logger


def get_content():
    global msgs, switch
    with open('AutoReplyContent.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
    msgs = [line.lstrip().rstrip() for line in lines]


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def file_reply(msg):
    global msgs
    sender = msg['User']['UserName'] if 'UserName' in msg['User'] else 'filehelper'
    if switch:
        for msg in msgs:
            itchat.send_msg(msg, sender)

# 自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global msgs, switch
    sender = msg['User']['UserName'] if 'UserName' in msg['User'] else 'filehelper'
    content = msg['Content']
    if switch:
        logger.info((msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper') + ': ' + content)
    if sender == 'filehelper':
        if content == '开启自动回复':
            switch = True
            itchat.send_msg('已开启自动回复！', sender)
        elif content == '关闭自动回复':
            switch = False
            itchat.send_msg('已关闭自动回复！', sender)
        else:
            itchat.send_msg('指令错误！', sender)
    else:
        if switch:
            for msg in msgs:
                itchat.send_msg(msg, sender)


global msgs, switch
switch = False
itchat.auto_login(hotReload=True, loginCallback=get_content)
itchat.run()
