# -*- coding=utf-8 -*-
# python35
from utils import *
from itchat.content import *
import itchat
import os

config_file = './config.ini'

# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def group_reply(msg):
    group_name = msg['User']['NickName']
    settings = get_config(file=config_file)
    group_enabled = settings['global']['group_enabled'].split(',')
    for group in group_enabled:
        if group in group_name or group_name in group:
            timestamp = get_timestamp()
            sender_name = msg['ActualNickName'] if msg['ActualNickName'] != '' else msg['User']['Self']['NickName']
            type = msg['Type'].upper()
            if type in ['TEXT', 'CARD', 'NOTE']:
                msg_content = msg['Content']
            elif type == 'MAP':
                msg_content = msg['Content'].split(':')[0] + '\t' + msg['Url']
            else:
                msg_content = msg['Text'] + '\t' + msg['Content']
            handle_new_folder(group_name)
            file = os.path.join('./records/{}/{}.log'.format(group_name, get_date()))
            content = '{}\t{}\t{}:\t{}\n'.format(timestamp, sender_name, type, msg_content)
            record(file, content)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def group_file_reply(msg):
    group_name = msg['User']['NickName']
    settings = get_config(file=config_file)
    group_enabled = settings['global']['group_enabled'].split(',')
    for group in group_enabled:
        if group in group_name or group_name in group:
            timestamp = get_timestamp()
            sender_name = msg['ActualNickName'] if msg['ActualNickName'] != '' else msg['User']['Self']['NickName']
            handle_new_folder(group_name)
            download_file = './records/{}/files/{}_'.format(group_name, timestamp) + msg.fileName
            msg.download(download_file)
            file = os.path.join('./records/{}/{}.log'.format(group_name, get_date()))
            content = '{}\t{}:\tsend file {}\n'.format(timestamp, sender_name, download_file)
            record(file, content)



if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run(debug=True)
