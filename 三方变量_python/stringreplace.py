#coding:utf-8

def find_repeat(source,elmt):  #字符串内特定元素的所有位置，针对单独字符串
    elmt_index=[]
    s_index = 0;e_index = len(source)
    while(s_index < e_index):
        try:
            temp = source.index(elmt,s_index,e_index)
            elmt_index.append(temp)
            s_index = temp + 1
        except ValueError:
            break
    return (elmt_index)

def string_replace(string,elmt_index,c):   #elmt_index为需要替换的下角标位置list，位置列表
    new = []
    for s in string:
        new.append(s)
    for index,point in enumerate(elmt_index): #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列
        new[point] = c
        # new[point] = c[index] #对应替换的字符列表，C为list
    return ''.join(new)

