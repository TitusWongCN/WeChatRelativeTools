# -*- coding=utf-8 -*-
# python37
from flask import Flask
import itchat

app = Flask('WeChatRecorder')
global private_groups, private_users


@app.route('/')
@app.route('/index')
def index():
    return '<h1>WeChatRecorder index page!</h1>'


@app.route('/<user>/<message>')
def send_message(user, message):
    if user in private_users:
        itchat.send_msg(message, private_users[user])
    else:
        for private_user in private_users:
            if user in private_user or user.upper() in private_user.upper():
                itchat.send_msg(message, private_users[private_user])
                break
    return 'OK'


@app.route('/group/<group_name>/<message>')
def send_group_message(group_name, message):
    if group_name in private_groups:
        itchat.send_msg(message, private_groups[group_name])
    else:
        for private_group in private_groups:
            if group_name in private_group or group_name.upper() in private_group.upper():
                itchat.send_msg(message, private_groups[private_group])
                break
    return 'OK'


def flush_friends():
    global private_groups, private_users
    private_groups = {}
    private_users = {}
    groups = itchat.get_chatrooms(update=True)
    for group in groups:
        private_groups[group['NickName']] = group['UserName']
    print(private_groups)
    friends = itchat.get_friends(update=True)
    for friend in friends:
        private_users[friend['NickName']] = friend['UserName']
    print(private_users)
    # itchat.run(debug=True)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, loginCallback=flush_friends)
    app.run('0.0.0.0', port=9999, debug=True)
