#coding:utf-8
import configparser
import happybase
import json
import requests
from query_sql import querysql


#检索数据
def get_rowkey_data(table, rowkey,columns=None):
    content = table.row(rowkey,columns=columns,include_timestamp=False)
    return (content)

#获取rowkey身份证和手机号
def find_rowkey():
    conf = configparser.ConfigParser()
    conf.read('data_type.ini')
    idcard = conf.get('Personal_information','idcard')
    mobile = conf.get('Personal_information', 'mobile')
    idcard = idcard[::-1]   #身份证反转
    mobile = mobile[::-1]   #手机号反转
    rowkey = idcard + mobile
    return (rowkey)


def get_rowkey():
    #连接hbase
    connection = happybase.Connection("10.0.4.143", timeout=50)
    #创建连接，通过参数size来设置连接池中连接的个数
    pool = happybase.ConnectionPool(size=5, host="10.0.4.143")
    #获取连接
    with pool.connection() as connection:
        # 获取table实例
        table_content = connection.table("user_variables_test")
        #查询数据row_start、row_stop：起始和终止rowkey，查询两rowkey间的数据
        #row_prefix：rowkey前缀，默认为None，即不指定前缀扫描，可传入前缀来扫描符合此前缀的行
        # include_timestamp是否返回时间戳
        #batch_size：用于检索结果的批量大小
        # for rowKey, history_data in table_content.scan(row_start=None, row_stop=None,include_timestamp=True,batch_size = 1000):
            #print(rowKey,history_data)
        content = get_rowkey_data(table_content,find_rowkey())
        #
        print(content[ b'variables:bqs_jk_rlid_369966'].decode('utf-8'))