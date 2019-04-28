#coding:utf-8
import json
import requests
from query_sql import querysql
from json_str import get_target_value
from 版本1.message import request_message
import jsonpath
import time
import configparser
import logging
#参考：https://www.cnblogs.com/nancyzhu/p/8551506.html

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

#发起请求
def post_requests(data_type_list):
    try:
        url = "http://10.0.4.147:8080/dubbo-rest/dubbo/send"
        headers = {"Content-Type": "application/json"}
        param = {'topic':'MQ_TOPIC_KAFKA_PROFILE_SYSTEM','message':request_message[data_type_list]}
        req = requests.post(url,param,headers)
        return req.text
    except:
        logging.info('dubbo接口异常，请核实！')


#获取dubbo接口字符串内容
def get_repose():
    url = "http://10.0.4.147:8080/dubbo-rest/dubbo/api?idcard=110000000000000015&mobile=13000000008"
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.get(url,headers)
        content = req.content
        json_str1 = json.loads(content)
        return (json_str1)
    except:
        logging.info('请求dubbo接口地址：{}异常！'.format(url))


#配置文件读取接口
def read_conf():
    conf = configparser.ConfigParser()
    conf.read('data_type.ini')
    data_type = []
    data_type_list = conf.get('Date_Type', 'date_type')
    if ',' in data_type_list:
         return (data_type_list.split(','))
    else:
         data_type.append(data_type_list)
         return (data_type)

#主程序
def solves_message():
    data_type_list = read_conf()
    for i in range(len(data_type_list)):
        logging.info('--------------------------------接口{}发起请求且开始效验！--------------------------------'.format(data_type_list[i]))
        post_requests(data_type_list[i])
        data_type = data_type_list[i].split('_')[0]
        intf_name = data_type_list[i].split('_')[1]
        variable_name, variable_type, calc_json_path,scope = querysql(data_type,intf_name)
        message = request_message[data_type_list[i]]
        message_json = json.loads(message)
        # print(message)
        for j in range(len(calc_json_path)):
            try:
               #logging.info(calc_json_path[i])
               value = jsonpath.jsonpath(message_json, calc_json_path[j])     #1.这里需要再次判断list内是否存在多值，如果多值就不能只取第1个，2.针对小数点需要判断只取2位，四舍五入
               # print(value,variable_name[j],calc_json_path[j])
               dubbovalue = get_target_value(variable_name[j], get_repose(), [])
               value1 = dubbovalue[0]['value']
               # 按照格式组装
               solves_value = '{"%s":{"scope":%s,"value":"%s"}' % (variable_name[j],scope[j], estimate(variable_type[j],value))  # 解析上传报文
               dubbo_value  = '{"%s":{"scope":%s,"value":"%s"}' % (variable_name[j],scope[j], value1)  # 解析dubbo接口报文
               if solves_value == dubbo_value:
                   logging.info("变量：{}一致，报文解析指：{}，dubbo解析值：{}".format(variable_name[j], solves_value, dubbo_value))
                   #pass
               elif '-' in solves_value:
                   if solves_value.replace('-', '') == dubbo_value:
                       logging.info("变量：{}一致，报文解析指：{}，dubbo解析值：{}".format(variable_name[j], solves_value, dubbo_value))
                       #pass
                   else:
                       logging.info("变量：{}不一致，报文解析指：{}，dubbo解析值：{}".format(variable_name[j], solves_value, dubbo_value))
               else:
                   logging.info("变量：{}不一致，报文解析指：{}，dubbo解析值：{}".format(variable_name[j],solves_value,dubbo_value))
            except:
                dubbovalue1 = get_target_value(variable_name[j], get_repose(), [])
                logging.info("变量：{}，报文解析异常，dubbo解析值：{}".format(variable_name[j],dubbovalue1[0]))
        logging.info('-----------------------------变量总数：{}个计算完毕！-----------------------------'.format(len(variable_name)))
        logging.info('\n')

#格式转化
def estimate(variable_type,value):
    if (variable_type == 'Numeric') and ('.' not in str(value)) :
        return (str(value)+'.0')
    elif variable_type == 'Date':
        return int(time.mktime(time.strptime(value, "%Y-%m")))
    elif (variable_type == 'Numeric') and ('.'  in str(value)):
        return (str(value))
    else:
        return value


if __name__ == '__main__':
   # post_requests()
   solves_message()
    #get_rowkey()