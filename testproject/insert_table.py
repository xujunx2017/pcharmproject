# coding:utf-8

import  pymysql
import random
db = pymysql.connect('10.0.4.141','user_profile','userprofile123','db_user_profile',charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cur = db.cursor()
#表名变量不能直接execute传入
#mobile = '130'+''.join((random.choice("0123456789") for i in range(8)))
#idcard = '42112'+''.join((random.choice("0123456789") for i in range(13)))
# event_happen_time ='2018-12-'+''.join(str(random.randint(1,31)))+' 14:48:18'
#print(event_happen_time)
index = int(input('请输入需要插入的条数：'))
for i in range(index):
    sql = "INSERT INTO `tb_user_apply_contact` (`name`, `mobile`, `idCard`, `urgent_contact_name`, `urgent_contact_mobile`, `contact_relationship`, `event_happen_time`, " \
          "`user_city`, `gps_city`, `employer`, `status`, `create_user`, `create_time`, `updeta_user`, `updeta_time`) VALUES " \
          "('景子霖{}', '{}', '{}', '我们', '{}', '2', '{}', '市辖区', '1', '闲情逸致', '1', NULL, " \
      "'2019-01-06 14:48:18', NULL, '2019-01-06 14:48:18');".format(str(i),'130'+''.join((random.choice("0123456789") for i in range(8))),'42112'+''.join((random.choice("0123456789") for i in range(13))),'131'+''.join((random.choice("0123456789") for i in range(8))),'2018-12-'+''.join(str(random.randint(1,31)))+' '+''.join(str(random.randint(1,23)))+':48:18')
    #执行sql语句
    cur.execute(sql)
    # 提交到数据库执行
    db.commit()
    #db.close()