#coding:utf-8
import requests
import re
import urllib.request
import os

def baidu_image(word,pn):
    headers = {
        "User - Agent": "Mozilla / 5.0(Windows NT 6.3;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36"
    }
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=" \
          "rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&" \
          "lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&" \
          "copyright=&word={}&s=&se=&tab=&width=&height=&face=0&" \
          "istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30&gsm=1e&1546674422335=".format(word,word,pn)
    res = requests.get(url,headers=headers,verify=False)
    if res.status_code == 200:
        return res.text
    else:
        return None

#获取图片url
def get_image(content,file,offset):
    pattern = re.compile('"thumbURL":"(.*?)"',re.S)
    img_list = pattern.findall(content)
    imgs = {}
    for index in img_list:
        print('开始下载第{}张图片：{}'.format(str(offset+1),index))
        urllib.request.urlretrieve(index,filename=file+'\\{}.jpg'.format(str(offset+1)))
        offset+=1

#主程序
def main(word,file,index):
    exiets_file(file)
    offset = 0
    for i in range(int(index)):
        pn = i*30
        content = baidu_image(word,pn)
        get_image(content,file,offset=offset*30)
        offset+=1


#判断文件夹是否存在
def exiets_file(file):
    if os.path.exists(file):
        return file
    else:
        os.mkdir(file)


if __name__ == '__main__':
    word = input('请输入需要查询的图片名字：')
    index = input('请输入需要下载的图片数量(默认*30，如输入2，则下载60张):{}:')
    file = os.getcwd() + '\\{}'.format(word)
    main(word,file,index)