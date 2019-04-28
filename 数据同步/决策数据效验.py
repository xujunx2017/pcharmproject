# coding:utf-8
######################
import requests
import  pymysql
from body_parms import request_body
import time

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
    print(req.text)
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
    #print(list)
    for xx in range(len(list)):
        print(list[xx]['mobile'])
        request_post = request_body(list[xx]['mobile'])
        #print(request_post)
        for i in range(len(request_post)):
            post_requests(request_post[i])
        time.sleep(10)
        table_loan_record = table_sql('rt_loan_record', list[xx]['mobile'], list[xx]['idcard'])
        print(table_loan_record)
        table_loan_record1 = table_sql('rt_loan_record1', list[xx]['mobile'], list[xx]['idcard'])
        print(table_loan_record1)
        try:
            for AA in range(len(table_loan_record)):
                #由于数据问题rt_loan_record1表数据比table_loan_record这个表数据少（同身份证和手机号）
                    if table_loan_record[AA]==table_loan_record1[AA]:
                        print("测试通过，测试环境 {}，生产环境{}".format(table_loan_record[AA],table_loan_record1[AA]))
                    else:
                        print("测试不通过，测试环境{}，生产环境{}".format(table_loan_record[AA],table_loan_record1[AA]))
        except Exception as e:
            print("身份证和手机号查询后，测试表数目：{}，生产表数目{}".format(len(table_loan_record),len(table_loan_record1)))
        print("\n")

# def open_list():
#     list = []
#     f = open(r'list.txt',encoding='utf-8')
#     for i in f.readlines():
#         content = i.split(',')
#         dict = {}
#         dict['idcard'] = content[0]
#         dict['mobile']=content[1].strip('\n')
#         list.append(dict)
#     #print(list)
#     for xx in range(len(list)):
#         print(list[xx]['mobile'])
#         request_post = request_body(list[xx]['mobile'])
#         for i in range(len(request_post)):
#             post_requests(request_post[i])
#         time.sleep(10)
#         table_loan_record = table_sql('rt_loan_record', list[xx]['mobile'], list[xx]['idcard'])
#         table_loan_record1 = table_sql('rt_loan_record1', list[xx]['mobile'], list[xx]['idcard'])
#         try:
#             for AA in range(len(table_loan_record)):
#                 #由于数据问题rt_loan_record1表数据比table_loan_record这个表数据少（同身份证和手机号）
#                     if table_loan_record[AA]['request_id']==table_loan_record1[AA]['request_id']:
#                         if table_loan_record[AA]['credit_blanace']==table_loan_record1[AA]['credit_blanace']:
#                             if table_loan_record[AA]['result']==table_loan_record1[AA]['result']:
#                                 if table_loan_record[AA]['rule_code'] == table_loan_record1[AA]['rule_code']:
#                                     print("测试通过：测试环境id = {}，生产环境id = {}".format(table_loan_record[AA]['id'],table_loan_record1[AA]['id']))
#                                 else:
#                                     print("rule_code不一致：测试环境id = {}，生产环境id = {}".format(table_loan_record[AA]['id'],table_loan_record1[AA]['id']))
#                             else:
#                                 print("result不一致：测试环境id = {}，生产环境id = {}".format(table_loan_record[AA]['id'],table_loan_record1[AA]['id']))
#                         else:
#                             print("credit_blanace不一致:测试环境credit_blanace = {}，生产环境credit_blanace = {}".format(table_loan_record[AA]['credit_blanace'],table_loan_record1[AA]['credit_blanace']))
#                     else:
#                         print("测试不通过，测试环境{}，生产环境{}".format(table_loan_record[AA],table_loan_record1[AA]))
#         except Exception as e:
#             print("身份证和手机号查询后，测试表数目：{}，生产表数目{}".format(len(table_loan_record),len(table_loan_record1)))
#         print("\n")

if __name__=="__main__":
    open_list()





