# -*-coding=utf8-*-
import configparser
import time
import os

def get_date():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

def get_timestamp():
    return time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))

def get_config(file='./config.ini'):
    settings = {}
    cp = configparser.ConfigParser()
    cp.read(file, encoding='utf8')
    for section in cp.sections():
        if section not in settings:
            settings[section] = {}
        for key, value in cp.items(section):
            if value in ['True', 'False']:
                value = True if value == 'True' else False
            settings[section][key] = value
    return settings

def handle_new_folder(group_name):
    if not os.path.isdir(os.path.join('./records/{}'.format(group_name))):
        os.system('mkdir "{}"'.format(os.path.join('./records/{}'.format(group_name))))
    if not os.path.isdir(os.path.join('./records/{}/files'.format(group_name))):
        os.system('mkdir "{}"'.format(os.path.join('./records/{}/files'.format(group_name))))

def record(file, content):
    with open(file, 'a', encoding='utf8') as f:
        f.write(content)
