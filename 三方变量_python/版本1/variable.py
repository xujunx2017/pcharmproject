#coding:utf-8
import requests
import json
from 版本1.conf import variable_txt
from json_str import get_target_value
from 版本1.message import request_message
import configparser
# r = requests.get("http://10.0.4.147:8080/dubbo-rest/dubbo/api?idcard=110000000000000015&mobile=13000000008")
# resp = r.content
# json_str = json.loads(resp)
#
# print(get_target_value('CK_APP_ApplLoanTime',json_str,[]))



#发起请求
def post_requests(data_typename):
    url = "http://10.0.4.147:8080/dubbo-rest/dubbo/send"
    headers = {"Content-Type": "application/json"}
    param = {'topic':'MQ_TOPIC_KAFKA_PROFILE_SYSTEM','message':request_message[data_typename]}
    req = requests.post(url,param,headers)
    return req.text

#print(variable_txt['zhongchengxin_trareport'])

#获取dubbo接口字符串内容
def get_repose():
    url = "http://10.0.4.147:8080/dubbo-rest/dubbo/api?idcard=110000000000000015&mobile=13000000008"
    headers = {"Content-Type": "application/json"}
    req = requests.get(url,headers)
    content = req.content
    json_str1 = json.loads(content)
    return json_str1
    #print(get_target_value('TianX_IdCard_Is', json_str1, []))

#打开接口名称配置文件
def open_ini():
    conf = configparser.ConfigParser()
    conf.read('data_type.ini')
    data_type_list = conf.get('Date_Type', 'date_type').split(',')
    for i in range(len(data_type_list)):
        post_requests(data_type_list[i])
        print("--------------------------------上报接口 {} 的报文成功 --------------------------------".format(data_type_list[i]))
        get_list(data_type_list[i])


#脚本开始执行
def get_list(data_typename):
    List = []
    list=variable_txt[data_typename]
    #print(list)
    for i in range(len(list)):
        #print(list[i])
        #获取所有变量添加到list
        List.append(list[i]['name'])
    #print(List)
    for m in range(len(List)):
        #print(List[m])
        #获取scope和value
        scope = list[m]['scope']
        value = list[m]['value']
        resurt =get_target_value(List[m],get_repose(),[])
        scope1 = resurt[0]['scope']
        value1 = resurt[0]['value']
        # print(scope)
        # print(value)
        #按照格式组装
        aaa = '{%s="scope":%s,"value":%s}'%(List[m],scope,value)
        bbb = '{%s="scope":%s,"value":%s}'%(List[m],scope1,value1)
        if aaa == bbb:
            pass
            #print("{}字段效验一致".format(List[m]))
        else:
            print(aaa,bbb)

    print("--------------------------------{}接口效验完毕，总共{}个变量--------------------------------".format('zhongchengxin_trareport',len(List)))



if __name__ == '__main__':
    open_ini()
#print(get_target_value('TianX_IdCard_Is', get_repose(), []))
