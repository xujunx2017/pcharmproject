#coding:utf-8
import requests
import re
import json
import os
import time
import urllib.request
import shutil

def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
              }
    res = requests.get(url,headers=headers,verify = False)
    if res.status_code == 200:
        return res.text
    else:
        print('返回失败，请查看网络！')

def page_content(file,content,offset):
    pattern = re.compile('<dd>.*?class="board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"'
                         '+><a.*?>(.*?)</a>.*?releasetime">(.*?)</p>',re.S)
    result1 = pattern.findall(content)
    #print(result1)
    dict = {}
    for item in result1:
        img_file = file + '\\{}.jpg'.format(str(offset+1))
        #print(item)
        urllib.request.urlretrieve(item[1],img_file)
        offset += 1
        dict['index'] = item[0]
        dict['pic_src'] = item[1]
        dict['name'] = item[2]
        #dict['star'] = item[3]
        dict['releasetime'] = item[3][5:]
        # dict['month-wish'] = item[5]
        # dict['total-wish'] = item[6]
        write_text(file,dict)

def write_text(file,content):
    with open(file +'\\maoyantop100.txt','a+',encoding="UTF-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def main(file,offset):
    url = 'https://maoyan.com/board/6?offset='+str(offset)
    content = get_url(url)
    #print(content)
    page_content(file,content,offset)

def exists_file(file):
    if os.path.exists(file):
        shutil.rmtree(file) #先移除文件夹再创建
        time.sleep(3)
        return os.mkdir(file)
    else:
        return os.mkdir(file)

#取出总页数
def page_num():
    url = 'https://maoyan.com/board/6'
    content = get_url(url)
    pattern = re.compile('<a class=.*?href=.*?>(\d+)</a>',re.S)
    page_num = pattern.findall(content)
    return page_num

#分页查询
def query_html(file):
    exists_file(file)
    total_page = len(page_num())
    #main(file, offset=2 * 10)
    for x in range(total_page):
        main(file,offset= x*10)

if __name__ == '__main__':
    file =os.getcwd()+'\\maoyantop100'
    query_html(file)
