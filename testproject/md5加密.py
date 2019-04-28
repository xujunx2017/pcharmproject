import hashlib

a = input('输入加密的字符:')   #python3为input
b = hashlib.md5()
b.update(a.encode(encoding='utf-8'))
print ('MD5加密前：'+ a)
print ('MD5加密后：'+b.hexdigest())

