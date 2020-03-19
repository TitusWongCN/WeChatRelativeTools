# -*- coding=utf-8 -*-
# python37
from collections import OrderedDict

wiki = ['天气: TQ+城市名', '空气质量: KQZL+城市名', '股票: GP+股票代码', '数字货币: SZHB+币种代码', '笑话: XH', '新闻: XW']
assistant = ['定时提醒: DSTX', '定时计划: DSJH', '备忘录: BWL+备忘录内容']
learning = ['CSDN文章: CSDN', '掘金文章: JJ']
entertainment = ['电影: DY+电影名',]
feedback = ['意见反馈: YJFK']
help = ['帮助: BZ']

help_menu = OrderedDict({
    '百科': wiki,
    '生活助手': assistant,
    '学习': learning,
    '娱乐': entertainment,
    '反馈': feedback,
    '帮助': help,
})

# 34 *
# 15 汉字
