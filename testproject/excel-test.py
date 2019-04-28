# coding:utf-8
import xlrd
from collections import OrderedDict
import json
import codecs
from datetime import datetime
from xlrd import xldate_as_tuple


#excel结果表内变量去校验testjson串
def get_excel():
    wb = xlrd.open_workbook(r"E:\22222\f414ebef-1e3e-4737-aa50-57d4a67f8340.xlsx")
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
    #print(convert_list)
    j = json.dumps(convert_list)
    #print(j)
    excel = json.loads(j)
    print(excel)


    f = open(r'E:\22222\f414ebef-1e3e-4737-aa50-57d4a67f8340.txt')
    content = f.read()
    json_str = json.loads(content)
    List = []
    single1 = OrderedDict()

    # 将变量转化为小写,并重新组装变量字典
    for key2 in json_str:
        for key3 in json_str[key2].keys():
            single1[key3.lower()] = json_str[key2][key3]
        List.append(single1)
        #print(List)

    # #List类型编码为str类型
    txt = json.dumps(List)
    #解码
    txt1 = json.loads(txt)

    # 校验2个文件的值
    for key4 in excel[0]:
         try:
             # 相等的值不打印
             if str(excel[0][key4]) == str(txt1[0][key4]):
                 pass
                 #print('变量名：%s,测试样本中的值："%s",excel中的值："%s"' % (key4, txt1[0][key4], excel[0][key4]))
             else:
                 print('变量名：%s,测试样本中的值："%s",excel中的值："%s"' % (key4, txt1[0][key4], excel[0][key4]))
                 #pass

         except Exception as e:
             #print('在测试样本中不存在%s变量' %e)
             print()





if __name__=="__main__":
    get_excel()
