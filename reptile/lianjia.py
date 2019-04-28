#coding=utf-8

import requests
import re
import json

def query_lianjia(rs_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    url = 'https://sz.lianjia.com/ershoufang/rs{}/'.format(rs_name)
    req = requests.get(url,headers=headers,verify=False)
    pattern = re.compile("page-data='(.*?)'",re.S)
    page_data = pattern.findall(req.text)
    total_index = json.loads(page_data[0])['totalPage']
    list = []
    for index in range(1,int(total_index)+1):
        url = 'https://sz.lianjia.com/ershoufang/pg{}rs{}/'.format(index,rs_name)
        req = requests.get(url, headers=headers, verify=False)  #verify=False不验证证书
        pattern = re.compile('class="title" href="(.*?)"', re.S)
        html = pattern.findall(req.text)
        list.append(html)
    html_list = []
    htmllist = list
    for index in range(len(htmllist)):
        # 删除元素
        htmllist[index].remove('<%=url%>')
        for items in htmllist[index]:
            html_list.append(items)
    print (html_list)
    print(len(html_list))

#多页html组装到一个list内
def main(rs_name):
    query_lianjia(rs_name)


def get_requests():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    html = 'https://sz.lianjia.com/ershoufang/105101208598.html'
    req = requests.get(html, headers=headers, verify=False)
    print(req.text)



if __name__ == '__main__':
    # rs_name = input('请输入需要查询的在售二手房小区名称：')
    # main(rs_name)
    get_requests()