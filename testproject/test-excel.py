# coding:utf-8
import xlrd
from collections import OrderedDict
import json
import codecs
from datetime import datetime
from xlrd import xldate_as_tuple


#test文本内json串变量提取出来，放到excel结果表，然后校验value
#test json串内变量效验excel结果表
def get_excel():
    wb = xlrd.open_workbook(r"E:\22222\测试样本13513543518.xlsx")
    convert_list = []
    #通过索引获取表格
    sh = wb.sheet_by_index(0)
    #获取表内容
    title = sh.row_values(0)
    keys = []
    # 获取表行数
    rows=sh.nrows
    # print(sh.nrows)
    # 获取表列数
    cols = sh.ncols
    # print(cols)
    #for rownum in range(1, sh.nrows):
    for i in range(rows):
        row_content = []
        for j in range(cols):
            #ctype： 0,empty, 1,string, 2,number, 3,date, 4,boolean, 5,error
            ctype = sh.cell(i, j).ctype  # 表格的数据类型
            #print(sh.cell(i, j),ctype)
            cell = sh.cell_value(i, j)
            if ctype == 2 and cell % 1 == 0:  # 如果是整形
                cell = int(cell)
            elif ctype == 3:
                # 转成datetime对象
                date = datetime(*xldate_as_tuple(cell, 0))
                cell = date.strftime('%Y/%d/%m %H:%M:%S')
            elif ctype == 4:
                cell = True if cell == 1 else False
            row_content.append(cell)
    #print(row_content)
    #  取出行数对应的值
    #rowvalue = sh.row_values(i)
    #print(rowvalue)
    single = OrderedDict()
    for colnum in range(0, len(row_content)):
        #print(title[colnum],row_content[colnum])
        #return (title[colnum],rowvalue[colnum])
        single[title[colnum]] = row_content[colnum]
    convert_list.append(single)
    j = json.dumps(convert_list)
    excel = json.loads(j)


    f = open(r'E:\22222\测试样本13513543518.txt', encoding='UTF-8')
    content = f.read()
    # print(content)
    json_str = json.loads(content)

    # 校验2个文件的值
    for key in json_str.keys():
        for kys1 in json_str[key].keys():
            try:
                if str(json_str[key][kys1]) == str(excel[0][kys1.lower()]):
                    pass
                else:
                    print('变量名：%s,测试样本中的值："%s",excel中的值："%s"' % (kys1, json_str[key][kys1], excel[0][kys1.lower()]))
            except Exception as e:
                print('在测试样本中不存在%s变量' % e)




if __name__=="__main__":
    get_excel()




