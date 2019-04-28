# coding:utf-8

import  pymysql
db = pymysql.connect('10.0.4.125','crs_data','eR3T58CsBnrAmobY','crs_data',charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cur = db.cursor()
#表名变量不能直接execute传入
table = input("请输入表名：")
value = ("id","id1","id2","id3","id4","id5","id6","id7","id8")
sql = """CREATE TABLE %s""" % table + """ (
          %s  int(11) NOT NULL,
          %s varchar(20) NOT NULL,
          %s varchar(20) NOT NULL,
          %s varchar(20) ,
          %s varchar(100),
          %s timestamp NOT NULL , 
          %s varchar(30) ,
          %s datetime ,
          %s varchar(30) )"""%value
cur.execute(sql)
