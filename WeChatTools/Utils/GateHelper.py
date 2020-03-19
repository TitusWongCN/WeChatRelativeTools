# -*- coding=utf-8 -*-
# python35
from Utils.GateAPI import GateIO


class GateHelper(object):
    def __init__(self, gate_api_url):
        self.gateio = GateIO(gate_api_url)
        self.gate_token_markets = self.get_pairs()

    def get_return_msg(self, content):
        try:
            token_name = content.split(',')[0]
            token_info = 'price' if len(content.split(',')) < 2 else content.split(',')[-1]
            token_para = ['token_pair'] if token_info == 'price' else content.split(',')[:-1]
            if token_name.upper() + '_USDT' in self.gate_token_markets:
                token_pair = token_name.upper() + '_USDT'
            else:
                # itchat.send_msg('指令不正确(目前只接受USDT交易区数据查询)!', test_group[group_name])
                return 'ERROR'
            token_para[0] = token_pair
            return self.exec_func(token_info, token_para)
        except:
            return 'ERROR'

    def exec_func(self, func_name, para=[]):
        if func_name == 'pairs':
            return self.get_pairs()
        elif func_name == 'price':
            token_pair = para[0]
            price_data = self.get_price(para)
            return '[{}]的当前价格为: \n[{}]\n24小时涨幅为[{}]\n数据来自gateio交易平台'.\
                format(token_pair, price_data[0], price_data[1])
        elif func_name == 'depth':
            token_pair, count = para if len(para) == 2 else [para[0], 5]
            return '[{}]当前的[{}]档深度为: \n{}\n数据来自gateio交易平台'.\
                format(token_pair, str(count), self.get_depth(para))

    def get_pairs(self):
        return self.gateio.pairs()


    def get_markets(self):
        return self.gateio.marketlist()

    def get_price(self, para):
        token_pair = para[0]
        data = self.gateio.ticker(token_pair)
        last_price = data['last']
        percent_change = '%.2f%%' % float(data['percentChange'])
        return last_price, percent_change

    def get_depth(self, para):
        # print(para)
        token_pair, count = para if len(para)==2 else [para[0], 5]
        count = 30 if int(count) > 30 else int(count)
        data = self.gateio.orderBook(token_pair)
        buy_data = data['bids'][:count]
        sell_data = data['asks'][0-count:]
        return_info = '\n'.join(['\t\t\t'.join(ticker) for ticker in sell_data])\
            + '\n-------------------------\n' + \
            '\n'.join(['\t\t\t'.join(ticker) for ticker in buy_data])
        return return_info





if __name__ == '__main__':
    gate_helper = GateHelper('data.gateio.co')
    markets = gate_helper.get_markets()
    print(markets['data'][0])
    markets = [market for market in gate_helper.get_markets()['data'] if market['curr_b'].upper() == 'USDT']

    result = [market['pair'].upper() for market in markets if int(market['vol_b'].replace(',', '')) > 75000]
    print(len(result))
    print(result)
    # print(gate_helper.get_price(['BOT_USDT', ]))
    # print(gate_helper.get_price('BCH_USDT'))
    # print(gate_helper.get_depth('BCH_USDT'))
    # print(gate_helper.exec_func('depth', ['BCH_USDT', 5]))



