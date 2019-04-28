#coding:utf-8

from 车贷变量数据效验.excel_variablename import get_variable
import json
from jsontest import get_target_value
import xlrd

#解析原始json
def get_json(variable_name):
    file = open(r'D:\pcharmproject\testproject\车贷变量数据效验\car_data_test_sample.txt', encoding='UTF-8')
    content = file.read()
    json_str = json.loads(content)
    value_json = []
    for index in range(len(json_str)):
        #print(json_str[index])get_variable
        value=get_target_value(variable_name,json_str[index],[])
        #value_json.append(value)
        if value == []:
            value_json.append('')
        else:
            value_json.append(value[0])
    return (value_json)


#获取结果表数据
def excel_value():
    wb = xlrd.open_workbook(r"D:\pcharmproject\testproject\车贷变量数据效验\临时数据提取20190123.xlsx")
    dict = {}
    variable_list = []
    # 通过索引获取表格
    for i in range(1):
        sh = wb.sheet_by_index(i)
        # 获取表行数
        rows = sh.nrows
        # 获取表列数
        cols = sh.ncols
        for j in range(cols):
            variable_name = sh.cell_value(0, j)
            variable_value = sh.cell_value(1, j)
            dict[variable_name] = variable_value
            variable_list.append(variable_name)
        return dict
        # print(dict)
        # print(dict['Apply_Code'.lower()])
        # print(dict['apply_code'])


def main():
    variable_list = get_variable()
    for index in range(len(variable_list)):
        #print(variable_list[index])
        variable_name = variable_list[index]
        for x in range(len(get_json(variable_name))):
            """
            txt_value:原始数据
            excel_value_v：结果数据

            """
            try:
                txt_value = str(get_json(variable_name)[x])
                excel_value_v = str(excel_value()[variable_name.lower()])
                aaa = '.0'
                if txt_value == excel_value_v:
                    print('变量：{}效验一致，原始json解析的值：{}，结果表值:{}'.format(variable_name, txt_value,
                                                                    excel_value_v))
                elif aaa  in  excel_value_v :
                    excel_value_v1 =excel_value_v[:-2]  #切片.0
                    if txt_value == excel_value_v1:
                        print('变量：{}效验一致，原始json解析的值：{}，结果表值:{}'.format(variable_name, txt_value,
                                                                         excel_value_v1))
                    else:
                        print('变量：{}效验不一致，原始json解析的值：{}，结果表值:{}'.format(variable_name, txt_value ,
                                                                           excel_value_v1))
                elif str(txt_value).count('.') ==1:   #判断小数
                    txt_value3 = '%.2f'%(float(txt_value))   #字符串转化为浮点型，保留2位小数
                    if txt_value3 == excel_value_v:
                        print('变量：{}效验一致，原始json解析的值：{}，结果表值:{}'.format(variable_name, txt_value3,
                                                                         excel_value_v1))
                    else:
                        print('变量：{}效验不一致，原始json解析的值：{}，结果表值:{}'.format(variable_name, txt_value3 ,
                                                                           excel_value_v))
                else:
                    print('变量：{}效验不一致，原始json解析的值：{}，结果表值:{}'.format(variable_name,txt_value ,excel_value_v))
            except:
                print('变量：{}出现异常，原始json解析的值：{}，结果表值:{}'.format(variable_name, txt_value ,
                                                                excel_value_v))








if __name__ == '__main__':
    main()