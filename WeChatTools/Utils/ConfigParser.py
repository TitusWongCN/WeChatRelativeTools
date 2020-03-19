# -*- coding=utf-8 -*-
# python35


class ConfigParser(object):
    def __init__(self, config_file, list_split_format, tuple_split_format):
        self.config_file = config_file
        self.list_split_format = list_split_format
        self.tuple_split_format = tuple_split_format

    def get(self, attr_name):
        with open(self.config_file, 'rb') as f:
            config_lines = f.read().decode('utf-8')
        for line in config_lines.split('\n'):
            if attr_name in line:
                line = line.replace(' ', '').lstrip().rstrip().strip()
                if attr_name == line.split('=')[0]:
                    data = line.split('=')[1]
                    if self.list_split_format in data:
                        temp = data.split(self.list_split_format)
                        return [(item.split(self.tuple_split_format)[0], item.split(self.tuple_split_format)[1])
                                if self.tuple_split_format in item else item for item in temp]
                    else:
                        return data

if __name__ == '__main__':
    config_parser = ConfigParser('../config.conf', '|&|', '|,|')
    print(config_parser.get('special_users'))
    print(config_parser.get('change_rate'))
    print(len(config_parser.get('change_rate')))
