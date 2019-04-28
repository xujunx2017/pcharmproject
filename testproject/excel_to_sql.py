# coding:utf-8
import pymysql
import xlrd


#sql = "SELECT * FROM cr_name_auth"
# 使用 execute()  方法执行 SQL 查询
#cur.execute(sql)beijing
# 使用 fetchone() 方法获取数据
#print(cur.fetchall())



#取出表格所有的数据
def excel(path,cur,table):
    wb = xlrd.open_workbook(path,'r')
    # 通过索引获取表格
    sh =wb.sheet_by_index(0)
    # 获取表行数
    rows = sh.nrows
    # 获取表列数
    cols = sh.ncols
    for i in range(0,rows):
        sqlstr= []
        for j in range(0,cols):
            # 读单元格数据sh.cell_value
            #print(sh.cell_value(i,j))
            sqlstr.append(sh.cell_value(i,j))
        valuestr = [int(sqlstr[0]), str(sqlstr[1]), str(sqlstr[2]), str(sqlstr[3]), str(sqlstr[4]), str(sqlstr[5]),
                    str(sqlstr[6]), str(sqlstr[7]), str(sqlstr[8])]
        # 表名table变量不能直接execute传入
        sql = "INSERT INTO %s" % table + " VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)"
        #执行sql语句
        cur.execute(sql, valuestr)


#创建数据库表
def create_table(cur,table,value):
    sql = """CREATE TABLE %s""" % table + """ (
              %s varchar(255) NOT NULL,
              %s varchar(255) NOT NULL,
              %s varchar(255) NOT NULL,
              %s varchar(255) ,
              %s varchar(255),
              %s varchar(255) NOT NULL , 
              %s varchar(30) ,
              %s varchar(255) ,
              %s varchar(255) )""" % value
    cur.execute(sql)

#数据库连接
def sql_connect(path,table, value):
    db = pymysql.connect('10.0.4.125','crs_data','eR3T58CsBnrAmobY','crs_data',charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()
    #执行创建数据库表
    create_table(cur, table, value)
    #执行excel数据存入table
    excel(path, cur, table)
    db.commit()  # 提交
    #  关闭两个连接
    cur.close()
    db.close()



if __name__=="__main__":
    path = "C:\\Users\\Administrator\\Desktop\\test.xls"
    table = input("请输入表名:")
    value = ("id", "name", "id_no", "compare_status", "compare_desc", "date_created", "created_by", "date_updated", "updated_by")
    sql_connect(path, table, value)

