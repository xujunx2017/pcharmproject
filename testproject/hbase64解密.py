# coding:utf-8
import base64
import json
import io
import gzip
from collections import OrderedDict


s=input("请输入已编码过的base64字符串:")

#base64解码
compresseddata = base64.b64decode(s)

#StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO
compressedstream = io.BytesIO(compresseddata)

#gzip解压缩
gzipper = gzip.GzipFile(fileobj=compressedstream,mode = 'rb')
data = gzipper.read()
#去掉b' '
print(data.decode('utf-8'))







