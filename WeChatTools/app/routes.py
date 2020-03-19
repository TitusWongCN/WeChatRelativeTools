# -*- coding=utf-8 -*-
# python35
from flask import request, url_for
from app import app
import time


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/recieve', methods=['get', 'post'])
def recieve():
    try:
        timestamp = request.values['timestamp']
        msg_from = request.values['msg_from']
        msg_content = request.values['msg_content']
        log_file = 'Log/Web-{}.log'.format(time.strftime('%Y%m%d', time.localtime(time.time())))
        with open(log_file, 'a') as f:
            f.write('{}\t{}: {}\n'.format(timestamp, msg_from, msg_content))
    except Exception as ex:
        return 'FAIL'
    return 'SUCCESS'


@app.route('/read', methods=['get', 'post'])
def read():
    try:
        log_file = 'Log/Web-{}.log'.format(time.strftime('%Y%m%d', time.localtime(time.time())))
        with open(log_file, 'r') as f:
            lines = f.readlines()
        content = '<br>'.join(lines)
    except:
        return 'FAIL'
    return content
