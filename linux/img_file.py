# -*- coding: utf-8 -*-：

import paramiko
import matplotlib.pyplot as plt
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')   #显示中文，中文不报错
# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

#连接linux执行命令
def con_linux(cmd):
    # 建立ssh连接
    ssh = paramiko.SSHClient()
    # 取消安全认证
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #连接Linux
    ssh.connect(hostname='10.0.4.147',port=22,username='root',password='Passw0rd')
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 读取执行结果
    result = stdout.readlines()
    return  result

 #主程序
def main(result,file):
    dict = {}
    cpu = []
    men = []
    time = []
    #print result[2:]
    for i in range(len(result[2:])):
        cpu_men = result[2:][i].strip('\n').split(" ")
        date_time = cpu_men[0]+' '+cpu_men[1]
        time.append(date_time)
        cpu.append(cpu_men[2])
        men.append(cpu_men[3])
        print("第{}次获取到的time：{}，cpu：{}，men：{}".format(i+1,date_time,cpu_men[2],cpu_men[3]))
        with open(file,'a+') as f:
            f.write(date_time+' '+cpu_men[2]+' '+cpu_men[3]+'\n')
    return cpu,men,time


# 绘图
def get_img(cpu,men,time):
    plt.title(u'cpu和内存占用率曲线图')
    plt.plot(time,cpu,color='green', label='cpu')
    plt.plot(time,men,color='red', label='men')
    plt.legend() # 显示图例
    plt.xlabel(u'时间')
    plt.ylabel(u'cpu和内存占比：（%）')
    plt.show()

def exists_file(file):
    if os.path.exists(file):
        os.remove(file)

if __name__ == '__main__':
    print("正式开始运行脚本......")
    file = 'cpu_men.txt'
    exists_file(file)
    pid = input('请输入需要监控的pid：')
    t = input('请输入次数：')
    cmd = 'sh ../home/xujun/test.sh {} {}'.format(str(pid),str(t))
    result = con_linux(cmd)
    cpu, men, time = main(result,file)
    get_img(cpu, men, time)
