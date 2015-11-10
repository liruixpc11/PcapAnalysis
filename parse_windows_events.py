# coding=UTF-8
from collections import namedtuple

import csv
import chardet


"""
Windows日志收集方案：
1. 部署LogParser
2. 在客户操作系统中通过LogParser导出系统日志为csv格式
3. 将导出的日志传回本地
4. 使用本脚本解析
"""


def parse_csv(event_csv, encoding='gbk'):
    with open(event_csv, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        header = reader.next()
        record_class = namedtuple("WindowsEventRecord", header)
        finished = False
        while not finished:
            try:
                yield record_class(*map(lambda x: x.decode(encoding), reader.next()))
            except StopIteration:
                finished = True


if __name__ == '__main__':
    for record in parse_csv("data/system_evt.csv"):
        print record.Strings
