# -*- coding=utf-8 -*-
# python35
import time


def get_short_timestamp():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def get_long_timestamp():
    return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
