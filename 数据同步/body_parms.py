#coding=utf-8
import pymysql
import time
import json
import os
def request_body(mobile):
    #连接数据库
    db = pymysql.connect('10.0.4.141','rts','m9ubQXsJ9D0p','rts',charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()
    #表名变量不能直接execute传入
    sql = 'SELECT * FROM `rt_apply_ext1` WHERE mobile = {}; '.format(mobile)
    cur.execute(sql)
    #print(sql)
    if os.path.exists('message.txt'):
        os.remove('message.txt')
    with open('message.txt','a+',encoding='utf-8') as file:
        file.write("[")
    x = 1
    for row in cur.fetchall():
        #print(row[5])
        with open('message.txt','a+',encoding='utf-8') as file:
            if x < cur.rowcount:
                #print(x)
                file.write(row[5]+','+"\n")
                x+=1
            else:
                file.write(row[5] +"\n")
                break
    with open('message.txt','a+',encoding='utf-8') as file:
        file.write("]")
    f = open(r'message.txt',encoding='utf-8')
    content = f.read()
    json_str = json.loads(content)
    #print(json_str)
    return json_str
