# -*- coding=utf-8 -*-
# python35
from Utils.GateTrendUpMonitor import TrendUpMonitor
from Utils.time_utils import get_long_timestamp
from Utils.ConfigParser import ConfigParser
from Utils.MailHelper import MailHelper
from Utils.GateHelper import GateHelper
from Utils.Logger import Logger
from itchat.content import *
import requests
import itchat
import os


def post_server(timestamp, msg_from, msg_content, server, method):
    url = server + method
    data = {
        'timestamp': timestamp,
        'msg_from': msg_from,
        'msg_content': msg_content
    }
    response = requests.post(url, data=data)
    return response.text


# 自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global private_users, private_groups, admin_users
    get_config_users()
    # 发送者的昵称
    sender_name = msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper'
    # 发送消息的内容
    content = str(msg['Text'])
    logger.logger.info('[text_reply] Message from {}:{}'.format(sender_name, content))
    if not sender_name == 'filehelper':
        try:
            post_server(get_long_timestamp(), sender_name, content, config_parser.get('prod_server_url'), 'recieve')
        except:
            print('post error!!!')
    for user in private_users:
        if user in sender_name:
            for admin in admin_users:
                itchat.send_msg(sender_name + ': ' + content, admin_users[admin])
    if sender_name in admin_users and '_' in content:
        message = content.split('_')[1]
        receiver = content.split('_')[0]
        if receiver == 'group':
            for group_name in private_groups:
                itchat.send_msg(message, private_groups[group_name])
                logger.logger.info('[text_reply] Send message to {}:{}'.format(group_name, message))
        else:
            if receiver in private_users:
                if len(message) == 17 and message[-4] == '.' and message[6] == '-':
                    if os.path.isfile('./filecache/' + message):
                        itchat.send_file('./filecache/' + message, private_users[receiver])
                        logger.logger.info('[text_reply] Forward message to {}:{}'
                                           .format(receiver, './filecache/' + message))
                    else:
                        for admin in admin_users:
                            itchat.send_msg('[text_reply] Forward message failed! Warning to {}: {} not exists!'
                                            .format(admin, './filecache/' + message), admin_users[admin])
                            logger.logger.info('[text_reply] Forward message failed! Warning to {}: {} not exists!'
                                            .format(admin, './filecache/' + message))
                else:
                    itchat.send_msg(message, private_users[receiver])
                    logger.logger.info('[text_reply] Forward message to {}:{}'.format(receiver, message))
    return_msg = gate_helper.get_return_msg(content)
    if return_msg != 'ERROR':
        logger.logger.info('[text_reply] Return message:{}'.format(return_msg))
        return return_msg


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def file_reply(msg):
    global private_users, admin_users
    get_config_users()
    sender_name = msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper'
    msg.download('./filecache/' + msg.fileName)
    logger.logger.info('[file_reply] Files recieved from:{}'.format(sender_name))
    for user in private_users:
        if user in sender_name:
            receiver = 'admin_users'
            break
        else:
            receiver = 'filehelper'
    if receiver == 'filehelper':
        logger.logger.info('[file_reply] Files forward to:{}'.format(receiver))
        if msg.type == 'PICTURE':
            itchat.send_image('./filecache/' + msg.fileName, receiver)
        elif msg.type == 'VIDEO':
            itchat.send_video('./filecache/' + msg.fileName, receiver)
        else:
            itchat.send_file('./filecache/' + msg.fileName, receiver)
    elif receiver == 'admin_users':
        logger.logger.info('[file_reply] Files forward to:{}'.format(receiver))
        for admin_user in admin_users:
            if msg.type == 'PICTURE':
                itchat.send_image('./filecache/' + msg.fileName, admin_users[admin_user])
            elif msg.type == 'VIDEO':
                itchat.send_video('./filecache/' + msg.fileName, admin_users[admin_user])
            else:
                itchat.send_file('./filecache/' + msg.fileName, admin_users[admin_user])


# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def group_text_reply(msg):
    global private_groups
    get_config_users()
    sender_name = msg['ActualNickName'] if msg['ActualNickName'] != '' else msg['User']['Self']['NickName']
    # 消息来自于哪个群聊
    group_name = msg['User']['NickName']
    # 发送消息的内容
    content = msg['Text']
    logger.logger.info('[group_text_reply] Message from {}:{}'.format(group_name, content))
    if group_name in private_groups.keys():
        group_id = private_groups[group_name]
        return_msg = gate_helper.get_return_msg(content)
        if return_msg != 'ERROR':
            return_msg = u'@{}\u2005\n' + return_msg
            itchat.send_msg(return_msg.format(sender_name), group_id)
            logger.logger.info('[group_text_reply] Return message:{}'.format(return_msg.format(sender_name)))
        else:
            if msg['IsAt']:
                return_msg = '@{}\u2005 我已收到消息:\n[{}]'.format(sender_name, content)
                itchat.send_msg(return_msg, group_id)
                logger.logger.info('[group_text_reply] Return message:{}'.format(return_msg))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def group_file_reply(msg):
    global private_groups
    get_config_users()
    msg.download('./filecache/' + msg.fileName)
    # 消息来自于哪个群聊
    group_name = msg['User']['NickName']
    logger.logger.info('[group_file_reply] Files recieved from:{}'.format(group_name))
    if group_name in private_groups.keys():
        group_id = private_groups[group_name]
        logger.logger.info('[group_file_reply] Files forward to:{}'.format('filehelper'))
        if msg.type == 'PICTURE':
            # itchat.send_image('./filecache/' + msg.fileName, group_id)
            itchat.send_image('./filecache/' + msg.fileName, 'filehelper')
        elif msg.type == 'VIDEO':
            # itchat.send_video('./filecache/' + msg.fileName, group_id)
            itchat.send_video('./filecache/' + msg.fileName, 'filehelper')
        else:
            # itchat.send_file('./filecache/' + msg.fileName, group_id)
            itchat.send_file('./filecache/' + msg.fileName, 'filehelper')


def get_config_users():
    global private_groups, private_users, admin_users
    logger.logger.info('[get_config_users] Flushing private_groups, private_users...')
    private_groups = {}
    private_users = {}
    admin_users = {}
    groups = itchat.get_chatrooms(update=True)
    special_groups = config_parser.get('special_groups')
    for group in groups:
        for special_group in special_groups:
            if special_group in group['NickName']:
                private_groups[group['NickName']] = group['UserName']
    friends = itchat.get_friends(update=True)
    special_users = config_parser.get('special_users')
    admins = config_parser.get('admin_users')
    for friend in friends:
        for special_user in special_users:
            if special_user in friend['NickName']:
                private_users[special_user] = friend['UserName']
        if isinstance(admins, str):
            if admins in friend['NickName']:
                admin_users[admins] = friend['UserName']
        else:
            for admin in admins:
                if admin in friend['NickName']:
                    admin_users[admin] = friend['UserName']


def start_monitor():
    global trend_monitor, private_groups, private_users, admin_users, mail_helper, config_parser, gate_helper, logger
    trend_monitor = TrendUpMonitor(private_groups, private_users, admin_users, mail_helper, config_parser, gate_helper, logger)
    trend_monitor.run()


if __name__ == '__main__':
    global trend_monitor, private_groups, private_users, admin_users, mail_helper, config_parser, gate_helper, logger
    config_parser = ConfigParser('./config.conf', '|&|', '|,|')
    logger = Logger()
    mail_helper = MailHelper(config_parser.get('my_sender'), config_parser.get('my_pass'))
    gate_helper = GateHelper(config_parser.get('gate_api_url'))
    itchat.auto_login(hotReload=True, loginCallback=get_config_users)
    start_monitor()
    itchat.run(debug=True)
