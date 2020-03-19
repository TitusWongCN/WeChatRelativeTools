# -*- coding=utf-8 -*-
# python37
from itchat.content import *
import itchat
from utils.wechat_wiki import get_weather

# 自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 发送者的昵称
    sender_name = msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper'
    # 发送消息的内容
    content = str(msg['Text'])
    if len(content.split(' ')) == 2:
        type = content.split(' ')[0]
        para = content.split(' ')[1]
        if type == '天气':
            return get_weather(para)
    elif len(content.split(' ')) == 1:
        type = content.replace('\n', '').replace('\r', '')
        if type == '帮助' or type.upper() == 'HELP' or type == 'BZ':
            return None
    elif len(content.split(' ')) == 3:
        pass


# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def file_reply(msg):
#     global private_users, admin_users
#     sender_name = msg['User']['NickName'] if 'NickName' in msg['User'] else 'filehelper'
#     msg.download('./filecache/' + msg.fileName)
#         for admin_user in admin_users:
#             if msg.type == 'PICTURE':
#                 itchat.send_image('./filecache/' + msg.fileName, admin_users[admin_user])
#             elif msg.type == 'VIDEO':
#                 itchat.send_video('./filecache/' + msg.fileName, admin_users[admin_user])
#             else:
#                 itchat.send_file('./filecache/' + msg.fileName, admin_users[admin_user])
#
#
# # isGroupChat=True表示为群聊消息
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
# def group_text_reply(msg):
#     sender_name = msg['ActualNickName'] if msg['ActualNickName'] != '' else msg['User']['Self']['NickName']
#     # 消息来自于哪个群聊
#     group_name = msg['User']['NickName']
#     # 发送消息的内容
#     content = msg['Text']
#     if msg['IsAt']:
#         return_msg = '@{}\u2005 我已收到消息:\n[{}]'.format(sender_name, content)
#         itchat.send_msg(return_msg, group_id)
#
#
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
# def group_file_reply(msg):
#     msg.download('./filecache/' + msg.fileName)
#     # 消息来自于哪个群聊
#     group_name = msg['User']['NickName']
#     if msg.type == 'PICTURE':
#         # itchat.send_image('./filecache/' + msg.fileName, group_id)
#         itchat.send_image('./filecache/' + msg.fileName, 'filehelper')
#     elif msg.type == 'VIDEO':
#         # itchat.send_video('./filecache/' + msg.fileName, group_id)
#         itchat.send_video('./filecache/' + msg.fileName, 'filehelper')
#     else:
#         # itchat.send_file('./filecache/' + msg.fileName, group_id)
#         itchat.send_file('./filecache/' + msg.fileName, 'filehelper')

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run(debug=True)
