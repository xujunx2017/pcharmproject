#coding:utf-8
# str = '1234567'
# # bbb = []
# # for i in range(len(str)):
# #     if i!=4:
# #         bbb.append(str[i])
# # aaa = '/'.join(bbb)
# #
# # #new_str = ''.join([str[i] for i in range(len(str)) if i!= 4])
# # print(aaa)
#
# new_str = str[:3]+'.'+str[3:]
# print(new_str)

# aaa = 1
# print(str(aaa)+'.0')

# import time
#
# a = "2018-12"
#
# #转化为数组
#
# timeArray = time.strptime(a, "%Y-%m")
#
#  #转换为时间戳
#
# timeStamp = int(time.mktime(timeArray))#1524822540
# print(timeStamp)

aaa = 'BaiQS_Rules=$.strategySet[*].hitRules[*].ruleId'
bbb = aaa.index('$')
print(aaa[bbb:])

