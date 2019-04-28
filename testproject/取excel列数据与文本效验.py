# coding:utf-8
import xlrd
from collections import OrderedDict
import json
import codecs
from datetime import datetime
from xlrd import xldate_as_tuple

#效验testjson变量值是否符合excel提供的取值范围
wb = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\很好借决策引擎接口文档 (2).xlsx")
convert_list = []
#通过索引获取表格
for i in range(2):
    sh = wb.sheet_by_index(i)
    #获取表行数
    rows=sh.nrows
   # 获取表列数
    cols = sh.ncols
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
        single = OrderedDict()
        #print(row_content)
        single[row_content[0]]=[row_content[1]]
        convert_list.append(single)
    j=json.dumps(convert_list,ensure_ascii=False)
    excel = json.loads(j)
# print(excel)
# print(len(excel))


List1 = []
single1 = OrderedDict()
for i in range(len(excel)):
    for v,k in excel[i].items():
        single1[v] = excel[i][v]
List1.append(single1)
#print(List1)
j = json.dumps(List1,ensure_ascii=False)
excel2 = json.loads(j)
#print(excel2[0])



f = open(r'E:\22222\f414ebef-1e3e-4737-aa50-57d4a67f8340.txt')
content = f.read()
 # print(content)
json_str = json.loads(content)

# 校验2个文件的值
for key in json_str.keys():
    for kys1 in json_str[key].keys():
        try:
            if str(json_str[key][kys1]) in str(excel2[0][kys1]):
                pass
            elif str(excel2[0][kys1]) == "['待定-无字段']":
                pass
            elif str(excel2[0][kys1]) == "['待定']":
                pass
            elif str(excel2[0][kys1]) == "['99991231;小于当前日期']":
                pass
            else:
                print('变量名：%s,测试样本中的值："%s",excel中的值："%s"' % (kys1, json_str[key][kys1], excel2[0][kys1]))
        except Exception as e:
            #rint('在测试样本中不存在%s变量' % e)
            print()



