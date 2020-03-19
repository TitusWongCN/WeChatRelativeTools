# -*- coding=utf-8 -*-
# python35
from RecorderUtils.ConfigParser import ConfigParser
from itchat.content import *
from logging import handlers
import logging
from flask import Flask, url_for, request
import itchat

logger = logging.getLogger('WeChatRecorder')
logger.setLevel(level=logging.INFO)
handler = handlers.TimedRotatingFileHandler('./static/Log/recorder.log', when='D', backupCount=0, encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - LINE %(lineno)-d: %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
config_parser = ConfigParser('./RecorderUtils/config.conf', '|&|')


# 自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 发送者的昵称
    sender_name = msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper'
    # 发送消息的内容
    content = str(msg['Text'])
    logger.info('[Friend <{}>]: <{}>'.format(sender_name, content))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def file_reply(msg):
    msg.download('./static/FileCache/' + msg.fileName)
    sender_name = msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper'
    logger.info('[Friend <{}>]: <{}>'.format(sender_name, msg.fileName))


# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def group_text_reply(msg):
    if int(config_parser.get('is_group_open')):
        sender_name = msg['ActualNickName'] if msg['ActualNickName'] != '' else msg['User']['Self']['NickName']
        # 消息来自于哪个群聊
        group_name = msg['User']['NickName']
        # 发送消息的内容
        content = msg['Text']
        logger.info('[Group <{}>] {}: {}'.format(group_name, sender_name, content))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def group_file_reply(msg):
    if int(config_parser.get('is_group_open')):
        msg.download('./static/FileCache/' + msg.fileName)
        sender_name = msg['ActualNickName'] if msg['ActualNickName'] != '' else msg['User']['Self']['NickName']
        # 消息来自于哪个群聊
        group_name = msg['User']['NickName']
        logger.info('[Group <{}>] {}: {}'.format(group_name, sender_name, msg.fileName))


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run(debug=True)
