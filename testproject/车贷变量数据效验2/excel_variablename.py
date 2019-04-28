#coding:utf-8

import xlrd
from collections import OrderedDict
import json
from datetime import datetime
from xlrd import xldate_as_tuple


def get_variable():
    wb = xlrd.open_workbook(r"D:\pcharmproject\testproject\车贷变量数据效验2\车贷需要解析的变量.xlsx")
    convert_list = []
    variable_list = []
    variable_list1 = []
    #通过索引获取表格
    for i in range(1):
        sh = wb.sheet_by_index(i)
        #获取表行数
        rows=sh.nrows
       # 获取表列数
        cols = sh.ncols
        for i in range(rows):
            #print(i)
            for j in range(cols):
                #print(i,j)
                cell = sh.cell_value(i, j)
                variable_list.append(cell.strip(' '))
        return (variable_list)

if __name__ == '__main__':
    get_variable()