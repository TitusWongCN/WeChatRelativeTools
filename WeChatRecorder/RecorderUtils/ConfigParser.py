# -*- coding=utf-8 -*-
# python35


class ConfigParser(object):
    def __init__(self, config_file, split_format):
        self.config_file = config_file
        self.split_format = split_format

    def get(self, attr_name):
        with open(self.config_file, 'rb') as f:
            config_lines = f.read().decode('utf-8')
        for line in config_lines.split('\n'):
            if attr_name in line:
                line = line.replace(' ', '')
                if attr_name == line.split('=')[0]:
                    data = line.split('=')[1]
                    if self.split_format in data:
                        return data.split(self.split_format)
                    else:
                        return data

if __name__ == '__main__':
    config_parser = ConfigParser('../config.conf', '|&|')
    print(config_parser.get('special_users'))
