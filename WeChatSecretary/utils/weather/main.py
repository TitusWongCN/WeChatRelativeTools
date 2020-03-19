# -*- coding=utf-8 -*-
# python37
from utils.api_config import keys
from utils.general_model import call_api
import json


class Weather():
    def __init__(self, key_type, method, api, city_code_file='./utils/weather/amap_citycode.csv'):
        self.key = keys[key_type]
        self.method = method
        self.api = api
        self.city_code_file = city_code_file
        self.codes = self.get_city_code_dict()

    def get_city_code_dict(self):
        with open(self.city_code_file, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
        codes = {line.split(',')[0]: line.split(',')[1].replace('\n', '')  for line in lines}
        return codes

    def get_weather(self, city):
        # todo: 如何根据关键词搜索城市名称，比如根据无锡定位到无锡市
        if city in self.codes:
            city_code = self.codes[city]
        else:
            for city_name in self.codes:
                if city in city_name:
                    city_code = self.codes[city_name]
                    break
        paras = {
            'key': keys[key_type],
            'city': city_code
        }
        data = json.loads(call_api(self.api, paras, 'GET'))
        if data['infocode'] == '10000':
            spec = AmapWeatherSpec(data['forecasts'][0])
            return spec.to_string()


class AmapWeatherSpec():
    def __init__(self, json):
        self.province = json['province']
        self.city = json['city']
        self.reporttime = json['reporttime']
        self.casts = json['casts']

    def format_casts(self):
        str_casts = []
        for cast in self.casts:
            date = cast['date']
            dayweather = cast['dayweather']
            nightweather = cast['nightweather']
            daytemp = cast['daytemp']
            nighttemp = cast['nighttemp']
            daywind = cast['daywind']
            nightwind = cast['nightwind']
            daypower = cast['daypower']
            nightpower = cast['nightpower']
            # desc
            temp_desc = '{}℃~{}℃'.format(nighttemp, daytemp)
            weather_desc = dayweather if dayweather == nightweather else '{}转{}'.format(dayweather, nightweather)
            wind_desc = '{}风{}级'.format(daywind, daypower) if daywind + daypower == nightwind + nightpower else\
                '日间{}风{}级; 夜间{}风{}级'.format(daywind, daypower, nightwind, nightpower)
            # 汇总desc
            str_casts.append('{}气温{},{},{}'.format(date, temp_desc, weather_desc, wind_desc))
        return '\n'.join(str_casts)

    def to_string(self):
        forecast = self.format_casts()
        data = '\n'.join([self.province + self.city + '天气预报', forecast, '发布时间：' + self.reporttime])
        return data


key_type = 'amap'
method = 'GET'
api = 'https://restapi.amap.com/v3/weather/weatherInfo?extensions=all&'
weather = Weather(key_type, method, api)

if __name__ == '__main__':
    # weather = Weather(key_type, method, api, city_code_file='./amap_citycode.csv')
    result = weather.get_weather('无锡市')
    print(result)
