#coding:utf-8

from 车贷变量数据效验2.excel_variablename import get_variable
import json
from jsontest import get_target_value
import xlrd

#解析原始json
def get_json():
    file = open(r'D:\pcharmproject\testproject\车贷变量数据效验2\car_data_test_sample.txt', encoding='UTF-8')
    content = file.read()
    json_str = json.loads(content)
    json_dict = {}
    for key,value in json_str[0].items():
        if isinstance(value, dict):
            for key1,value1 in value.items():
                json_dict[key1.lower()] = value1
        elif key == 'applyCode':
            key = 'apply_code'
            json_dict[key] = value
        else:
            json_dict[key.lower()] = value
    return (json_dict)   #解析组合为dict

#获取结果表数据
def excel_value():
    wb = xlrd.open_workbook(r"D:\pcharmproject\testproject\车贷变量数据效验2\临时数据提取20190123.xlsx")
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
        return (dict)


def main():
    variable_list = get_variable()
    count = 0
    for index in range(len(variable_list)):
        #print(variable_list[index])
        variable_name = variable_list[index]
        count+=1
        #print(variable_name)
        """
        txt_value:原始数据
        excel_value_v：结果数据
        
        """
        if variable_name in get_json():
            txt_value = str(get_json()[variable_name]).replace(' ','').lower()
            excel_value_v = str(excel_value()[variable_name]).lower()
            aaa = '.0'
            if txt_value== excel_value_v:
                pass
                    # print('开始效验第{}个变量：{}效验一致，原始json解析的值：{}，结果表值:{}'.format(count,variable_name, txt_value,excel_value_v))
            elif aaa in excel_value_v:
                excel_value_v1 = excel_value_v[:-2]  # 切片.0
                if txt_value == excel_value_v1:
                    pass
                    # print('开始效验第{}个变量：{}效验一致，原始json解析的值：{}，结果表值:{}'.format(count,variable_name, txt_value,
                    #                                                excel_value_v1))
                else:
                    print('开始效验第{}个变量：{}效验不一致，原始json解析的值：{}，结果表值:{}'.format(count,variable_name, txt_value,
                                                                    excel_value_v1))
            else:
                    print('开始效验第{}个变量：{}效验不一致，原始json解析的值：{}，结果表值:{}'.format(count,variable_name, txt_value,excel_value_v))
        else:
            print('开始效验第{}个变量变量：{}不存在,结果表值:{}'.format(count,variable_name,str(excel_value()[variable_name])))

if __name__ == '__main__':
    main()