#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from multiprocessing import Manager, Pool
import happybase
import re
import requests
import json
import datetime
import logging
import sys
import os
import time



# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
LOG_FILENAME = 'logging_rotatingfile.out'

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')  # 控制台格式控制
# 文件日志
file_handler = logging.FileHandler(LOG_FILENAME)
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
file_handler.setLevel(logging.INFO)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
console_handler.setLevel(logging.INFO)
# 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# 指定日志的最低输出级别，默认为WARN级别


# util.log_to_stderr(level=logger.DEBUG)

data_list = []

headers = {"Content-type": "application/json", 'Connection': 'close'}
thrift_url = "10.0.4.143"
# hbase_url = "http://10.0.4.149:8088/report/gateway"
# encrypyt_url = "http://10.0.4.52:8000/Utils/Encrypt?plaintext="
# decrypyt_url = "http://10.0.4.52:8000/Utils/Decrypt?cipher="

# thrift_url = 'datayun19'
# hbase_url = "http://creditreport.touna.cn/report/gateway"
# encrypyt_url = "http://172.30.19.251:8000/Utils/Encrypt?plaintext="
# decrypyt_url = "http://172.30.19.251:8000/Utils/Decrypt?cipher="

"同盾、天行、大蜂、上海资信,宜信"

row_start1=None
row_stop1='57f3d1a99c7d43dda51edf5612744432'
row_start2='57f3d1a99c7d43dda51edf5612744432'
row_stop2=None

def get_rowkey_data(table, rowkey,columns=None):
    content = table.row(rowkey,columns=columns,include_timestamp=False)
    return content


def get_rowkey(path,row_start,row_stop,begin_date,end_date):
    with open(path, "w") as f:
        logger.info('write date to %s'%path)
        success_times = 0
        with pool.connection() as connection:
            crs_history_report = connection.table("crs_history_report")
            for rowKey, history_data in crs_history_report.scan(row_start=row_start, row_stop=row_stop,
                                                                include_timestamp=True, batch_size=200):

                try:
                    timestamp = history_data['history:serviceName'][1]  # 数据有异常
                except:
                    # logger.error('some exception happen', exc_info=True)
                    # logger.info('error data%s'%history_data)
                    continue
                date_local = datetime.date.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d")  # 数据生成的时间
                if date_local >= begin_date and date_local < end_date:
                    print(rowKey)
                    content = get_rowkey_data(crs_history_report,rowKey)
                    print('content',content)
                    #f.write(rowKey + '\n')
                    success_times += 1
                    if success_times % 10000 == 0:
                        logger.info('success times %s' % success_times)
                else:
                    continue




def isVaildDate(str_date):
    try:
        standard_date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
        return standard_date
    except:
        logger.error('时间格式不正确，正确格式为   %Y-%m-%d %Y-%m-%d')


if __name__ == '__main__':
    argument=['2018-01-01','2018-11-01']
    rowkey_path = './rowkeyfile/'
    # try:
    #     argument[0] =sys.argv[1]
    #     argument[1] =sys.argv[2]
    # except:
    #     logger.error('输入时间参数，正确格式为   %Y-%m-%d %Y-%m-%d')
    #     sys.exit()
    connection = happybase.Connection(thrift_url, timeout=50)

    if isVaildDate(argument[0]) < isVaildDate(argument[1]):
        begin_date = argument[0]
        end_date = argument[1]
        logger.info("开始执行程序")
        pool = happybase.ConnectionPool(size=3, host=thrift_url)
        get_rowkey('rowkey_file_1.txt',row_start1,row_stop1,begin_date,end_date)
        get_rowkey('rowkey_file_2.txt',row_start2,row_stop2,begin_date,end_date)
    else:
        logger.error('起始时间必须小于截至时间   %Y-%m-%d %Y-%m-%d')
        sys.exit()
