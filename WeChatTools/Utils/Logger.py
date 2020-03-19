# -*- coding=utf-8 -*-
# python35
import logging
from Utils import time_utils


class Logger(object):
    def __init__(self):
        logger = logging.getLogger('WeChatRobot')
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler('./Log/Monitor-{}.log'.format(time_utils.get_short_timestamp()), encoding="UTF-8")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - LINE %(lineno)-d: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

