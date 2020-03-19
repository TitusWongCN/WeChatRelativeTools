# -*- coding=utf-8 -*-
# python37
import requests


def call_api(url, paras, method):
    if method == 'GET':
        paras = '&'.join([str(k) + '=' + str(v) for k, v in paras.items()])
        data = requests.get(url + paras).text
    elif  method == 'POST':
        data = requests.post(url, data=paras).text
    else:
        data = 'Data error!'
    return data


