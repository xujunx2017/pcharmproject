# coding:utf-8
#针对hbase取数据
import requests
import  pymysql
import time
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


#检索数据
def get_rowkey_data(table, rowkey,columns=None):
    content = table.row(rowkey,columns=columns,include_timestamp=False)
    return (content)

def find_rowkey(mobile):
    list = []
    db = pymysql.connect('10.0.4.141','rts','m9ubQXsJ9D0p','rts',charset='utf8')
    cur = db.cursor()
    sql = 'SELECT * FROM `rt_apply_ext1` where mobile = {};'.format(mobile)
    cur.execute(sql)
    #print("sql",sql)
    for raw in cur.fetchall():
        row_key = raw[1] + '-' +raw[2]
        list.append(row_key)
    return (list)

def get_rowkey(mobile):
    #连接hbase
    connection = happybase.Connection("10.0.4.143", timeout=50)
    #创建连接，通过参数size来设置连接池中连接的个数
    pool = happybase.ConnectionPool(size=5, host="10.0.4.143")
    #获取连接
    with pool.connection() as connection:
        # 获取table实例
        table_content1 = connection.table("rts_decision_stevetao")
        #查询数据row_start、row_stop：起始和终止rowkey，查询两rowkey间的数据
        #row_prefix：rowkey前缀，默认为None，即不指定前缀扫描，可传入前缀来扫描符合此前缀的行
        # include_timestamp是否返回时间戳
        #batch_size：用于检索结果的批量大小
        # for rowKey, history_data in table_content.scan(row_start=None, row_stop=None,include_timestamp=True,batch_size = 1000):
            #print(rowKey,history_data)
        List = find_rowkey(mobile)
        #print(List,"List")
        request_content = get_rowkey_data(table_content1,List[0])
        #print('request_content',request_content)
        content_msg_test = request_content[b'cf1:requestMsg'].decode('utf-8')
    return content_msg_test

#发起请求
def post_requests(mesaage):
    url = "http://10.0.4.149:8893/rts/invoke"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    param = {'clazz':'com.touna.rts.modules.controller.test.TestController',
             'method':'基础资料环节',
             'params':'{}'.format(mesaage),
             'types':'java.lang.String'
             }
    req = requests.post(url,data=param,headers=headers)
    print("报文返回结果：{}".format(req.text))
    return (req.text)


def table_sql(table,mobile,id_no):
    db = pymysql.connect('10.0.4.141','rts','m9ubQXsJ9D0p','rts',charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()
    #表名变量不能直接execute传入
    sql = "SELECT * FROM `{}` WHERE mobile = '{}' AND id_no = '{}'ORDER BY end_time DESC;".format(table,mobile,id_no)
    cur.execute(sql)
    List = []
    request_id = []
    credit_blanace = []
    rule_code= []
    result= []
    id = []
    for raw in  cur.fetchall():
        #id.append(raw[0])
        request_id.append(raw[1])
        result.append(raw[10])
        credit_blanace.append(raw[15])
        rule_code.append(raw[22])
    #组装
    for key in range(cur.rowcount):
        dict= {}
        #print(key)
        #dict['id'] = id[key]
        dict['request_id'] = request_id[key]
        dict['credit_blanace'] = credit_blanace[key]
        dict['rule_code'] = rule_code[key]
        dict['result'] = result[key]
        List.append(dict)
    return List



def open_list():
    list = []
    f = open(r'list.txt',encoding='utf-8')
    for i in f.readlines():
        content = i.split(',')
        dict = {}
        dict['idcard'] = content[0]
        dict['mobile']=content[1].strip('\n')
        list.append(dict)
    print(list,'list')
    for xx in range(len(list)):
        print("mobile:{}".format(list[xx]['mobile']))
        mobile = list[xx]['mobile']
        mesaage = get_rowkey(mobile)
        print("请求报文:{}".format(mesaage))
        post_requests(mesaage)

    time.sleep(10)
    table_loan_record = table_sql('rt_loan_record', list[xx]['mobile'], list[xx]['idcard'])
    print(table_loan_record)
    table_loan_record1 = table_sql('rt_loan_record1', list[xx]['mobile'], list[xx]['idcard'])
    print(table_loan_record1)
    try:
        for AA in range(len(table_loan_record)):
            # 由于数据问题rt_loan_record1表数据比table_loan_record这个表数据少（同身份证和手机号）
            if table_loan_record[AA] == table_loan_record1[AA]:
                print("测试通过，测试环境 {}，生产环境{}".format(table_loan_record[AA], table_loan_record1[AA]))
            else:
                print("测试不通过，测试环境{}，生产环境{}".format(table_loan_record[AA], table_loan_record1[AA]))
    except Exception as e:
        print("身份证和手机号查询后，测试表数目：{}，生产表数目{}".format(len(table_loan_record), len(table_loan_record1)))
    print("\n")


if __name__=="__main__":
    open_list()





