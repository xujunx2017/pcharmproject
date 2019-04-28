#coding:utf-8
import pymysql
from stringreplace import find_repeat,string_replace

def querysql(data_type,intf_name):
    db = pymysql.connect('10.0.4.141', 'user_profile', 'userprofile123', 'db_user_profile', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()
    # 表名变量不能直接execute传入
    sql = "SELECT * FROM `up_variable` A WHERE A.data_type = '{}' AND A.intf_name = '{}'".format(data_type,intf_name)
    #print(sql)
    cur.execute(sql)
    variable_name = []
    calc_json_path = []
    variable_type = []
    scope = []
    for raw in cur.fetchall():
        #获取变量名
        variable_name.append(raw[8])
        #获取变量类型
        variable_type.append(raw[9])
        scope.append(raw[25])
        #'$.result'加点
        index_path = raw[13].index('$')  # 判断取值路径$符号的位置
        #raw[13][index_path+2] !='.'判断..在后面
        if '..' in raw[13][index_path:] and raw[13][index_path+2] !='.': #[index_path:]去掉$符号前面的内容,
            #获取变量取值路径
            calc_json_path.append(raw[13][index_path:][:2]+"."+raw[13][index_path:][2:])
        # raw[13][index_path+2] ='.'判断..在前面
        elif '..' in raw[13][index_path:] and raw[13][index_path+2] =='.':
            Reverse_order_index = raw[13][::-1].index('.')  # 字符串倒序找出.的下脚标位置
            order_index = len(raw[13][index_path:]) - Reverse_order_index  # 计算出顺序.的下脚标位置
            calc_json = raw[13][index_path:][:order_index-1]+'.'+raw[13][index_path:][order_index-1:]
            calc_json_path.append(calc_json)
        #针对表达式只有1个点 如：'$.FundDisburseAllCount'
        elif raw[13][::].index('.') == (len(raw[13])-raw[13][::-1].index('.')-1):
            calc_json =  raw[13][index_path:][:2]+"."+raw[13][index_path:][2:]
            calc_json_path.append(calc_json)
        else:
            #针对表达式存在多个.，如：‘$.gjj_detail[*].record_month’
            Reverse_order_index = raw[13][::-1].index('.')  # 字符串倒序找出.的下脚标位置
            order_index = len(raw[13][index_path:]) - Reverse_order_index  # 计算出顺序.的下脚标位置
            calc_json = raw[13][index_path:][:2] + '.' + raw[13][index_path:][2:order_index - 1] + '.' + raw[13][
                                                                                                         index_path:][
                                                                                                         order_index - 1:]
            calc_json_path.append(calc_json)
    return (variable_name, variable_type, calc_json_path, scope)

if __name__ == '__main__':
    querysql('wuyi','gjj')