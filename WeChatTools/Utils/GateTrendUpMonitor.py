# -*- coding=utf-8 -*-
# python35
from Utils.time_utils import get_long_timestamp
import traceback
import threading
import itchat
import time


class TrendUpMonitor(object):
    def __init__(self, private_groups, private_users, admin_users, mail_helper, config_parser, gate_helper, logger):
        self.private_groups = private_groups
        self.private_users = private_users
        self.admin_users = admin_users
        self.mail_helper = mail_helper
        self.gate_helper = gate_helper
        self.logger = logger
        self.monitor_special = config_parser.get('monitor_special')
        self.monitor_volumn_filter = int(config_parser.get('monitor_volumn_filter'))
        self.change_rate = config_parser.get('change_rate')
        self.monitor_scope = self.get_monitor_scope()


    def get_monitor_scope(self):
        markets = [market for market in self.gate_helper.get_markets()['data']
                   if market['curr_b'].upper() == 'USDT']
        filtered_scope = [market['pair'].upper() for market in markets
                if int(market['vol_b'].replace(',', '')) > self.monitor_volumn_filter]
        for special in self.monitor_special:
            if special not in filtered_scope and len(special) > 0:
                filtered_scope.append(special)
        print(filtered_scope)
        return filtered_scope


    def monitor(self, time_span, change_rate):
        self.pre_price = {token_pair: [0.0, 0.0] for token_pair in self.monitor_scope}
        self.is_init = True
        while True:
            for token_pair in self.pre_price:
                # print(token_pair, time_span, change_rate)
                try:
                    price = float(self.gate_helper.get_price([token_pair,])[0])
                    if price == 0.0:
                        continue
                    if self.is_init:
                        self.pre_price[token_pair] = [price, price]
                    else:
                        self.pre_price[token_pair][0] = self.pre_price[token_pair][1]
                        self.pre_price[token_pair][1] = price
                    percent_change = self.pre_price[token_pair][1]/self.pre_price[token_pair][0] - 1
                    if abs(percent_change) > float(change_rate):
                        # print(token_pair, self.pre_price[token_pair], percent_change)
                        format_up_str = '!!!!!!!!!!暴涨警报!!!!!!!!!!\n[{}]在[{}]秒内涨幅: [{}]\n最新价格为[{}]\n数据来自gateio交易平台'
                        format_down_str = '!!!!!!!!!!暴跌警报!!!!!!!!!!\n[{}]在[{}]秒内跌幅: [{}]\n最新价格为[{}]\n数据来自gateio交易平台'
                        if percent_change > 0:
                            message = format_up_str.format(token_pair, time_span, '%.2f%%' % (percent_change*100),
                                                           self.pre_price[token_pair][1])
                        else:
                            message = format_down_str.format(token_pair, time_span, '%.2f%%' % (percent_change*100),
                                                             self.pre_price[token_pair][1])
                        self.logger.logger.info('[TrendUpMonitor.monitor] message: {}'.format(message))
                        for admin in self.admin_users:
                            itchat.send_msg(message, self.admin_users[admin])
                            self.logger.logger.info('[TrendUpMonitor.monitor] Send message to: {}'.format(admin))
                        for group_name in self.private_groups:
                            itchat.send_msg(message, self.private_groups[group_name])
                            self.logger.logger.info('[TrendUpMonitor.monitor] Send message to: {}'.format(group_name))
                        # for user_name in self.private_users:
                        #     itchat.send_msg(message, self.private_users[user_name])
                        #     self.logger.logger.info('[TrendUpMonitor.monitor] Send message to: {}'.format(user_name))
                except Exception as ex:
                    print(traceback.format_exc())
                    self.logger.logger.error(traceback.format_exc())
                    continue
            self.is_init = False
            print('{}\t系统将会在[{}]秒后刷新币种涨幅信息...'.format(get_long_timestamp(), time_span))
            time.sleep(int(time_span))

    def run(self):
        for index in range(len(self.change_rate)):
            t = threading.Thread(target=self.monitor, args=(self.change_rate[index][0], self.change_rate[index][1]))  # 开启并行线程
            t.setDaemon(True)
            t.start()

