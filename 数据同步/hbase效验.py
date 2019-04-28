#!/usr/bin/env python
# -*- coding: utf-8 -*-

import happybase
import pymysql


# # create logger
# logger = logging.getLogger('MyLog')
# logger.setLevel(logging.DEBUG)
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# # add formatter to ch
# ch.setFormatter(formatter)
# # add ch to logger
# logger.addHandler(ch)
#
#
#
# thrift_url = "10.0.4.143"
# row_start1=None
# row_stop1='57f3d1a99c7d43dda51edf5612744432'
# #row_start2='57f3d1a99c7d43dda51edf5612744432'
# row_stop2=None
#
#
#
# # logger = logging.getLogger('MyLog')
# # logger.setLevel(logging.INFO)

#检索数据
def get_rowkey_data(table, rowkey,columns=None):
    content = table.row(rowkey,columns=columns,include_timestamp=False)
    return (content)

def get_rowkey():
    #连接hbase
    connection = happybase.Connection("10.0.4.143", timeout=50)
    #创建连接，通过参数size来设置连接池中连接的个数
    pool = happybase.ConnectionPool(size=5, host="10.0.4.143")
    #获取连接
    with pool.connection() as connection:
        # 获取table实例
        table_content1 = connection.table("rts_decision_stevetao")
        table_content = connection.table("rts_decision")
        #查询数据row_start、row_stop：起始和终止rowkey，查询两rowkey间的数据
        #row_prefix：rowkey前缀，默认为None，即不指定前缀扫描，可传入前缀来扫描符合此前缀的行
        # include_timestamp是否返回时间戳
        #batch_size：用于检索结果的批量大小
        # for rowKey, history_data in table_content.scan(row_start=None, row_stop=None,include_timestamp=True,batch_size = 1000):
            #print(rowKey,history_data)
        List = find_rowkey()
        for x in range(len(List)):
            content1 = get_rowkey_data(table_content1,List[x])
            content = get_rowkey_data(table_content, List[x])
            #logger.info(history_data[b'cf1:mobile'][0].decode('utf-8'))
            #print(content[b'cf1:responseMsg'].decode('utf-8'))
            content_msg_test = content[b'cf1:mobile'].decode('utf-8')
            content_msg_production = content1[b'cf1:mobile'].decode('utf-8')
            if content_msg_test == content_msg_production:
                print("rowkey：{}，生产和测试环境一致，测试通过".format(List[x]))
            else:
                print("测试环境：{}，生产环境：{}，测试不不通过".format(content_msg_test,content_msg_production))


def find_rowkey():
    list = []
    db = pymysql.connect('10.0.4.141','rts','m9ubQXsJ9D0p','rts',charset='utf8')
    cur = db.cursor()
    sql = 'SELECT * FROM `rt_apply_ext1`;'
    cur.execute(sql)
    for raw in cur.fetchall():
        row_key = raw[1] + '-' +raw[2]
        list.append(row_key)
    return (list)


if __name__ == '__main__':
    get_rowkey()
