# -*- coding=utf-8 -*-
# python35
from flask import Flask, url_for, request
import itchat


app = Flask('WeChatRecorder')
global private_groups, private_users
new_itchat = itchat.new_instance()


def login_warning():
    itchat.send_msg('WeChat is logging in now!', 'filehelper')


@app.route('/')
@app.route('/index')
def index():
    return '<h1>WeChatRecorder index page!</h1>'


@app.route('/log/<filename>', methods=['GET', 'POST'])
def display_log(filename):
    if request.method == 'GET':
        return 'ERROR! GET METHOD IS NOT ALLOWED!'
    if request.method == "POST":
        if request.form['key'] == 'youneverguess':
            with open('./static/Log/%s' % filename, 'r') as f:
                content = f.readlines()
            return '<br>'.join(content)


@app.route('/file/<filename>', methods=['GET', 'POST'])
def display_file(filename):
    if request.method == 'GET':
        return 'ERROR! GET METHOD IS NOT ALLOWED!'
    if request.method == "POST":
        if request.form['key'] == 'youneverguess':
            return url_for('static', filename='FileCache/%s' % filename)


@app.route('/<user>/<message>')
def send_message(user, message):
    if user in private_users:
        new_itchat.send_msg(message, private_users[user])
    else:
        for private_user in private_users:
            if user in private_user or user.upper() in private_user.upper():
                new_itchat.send_msg(message, private_users[private_user])
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
    groups = new_itchat.get_chatrooms(update=True)
    for group in groups:
        private_groups[group['NickName']] = group['UserName']
    print(private_groups)
    friends = new_itchat.get_friends(update=True)
    for friend in friends:
        private_users[friend['NickName']] = friend['UserName']
    print(private_users)


if __name__ == '__main__':
    new_itchat.auto_login(hotReload=True, loginCallback=flush_friends, statusStorageDir='itchat.pkl')
    app.run('0.0.0.0', port=8888, debug=True)
