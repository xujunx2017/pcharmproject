#!/bin/bash

echo '开始清理文件:cpu_men.log'
rm -f cpu_men.log

echo '开始运行脚本test.sh'
pid=$1
for((i=1;i<=$2;i++));
do
#由于-d 刷新间隔未生效，所以使用sleep
top -p $pid -b -d 120 -n 1|grep $pid |awk '{print strftime("%Y-%m-%d %H:%M:%S"),$9,$10}'>>cpu_men.log
echo `top -p $pid -b -d 120 -n 1|grep $pid |awk '{print strftime("%Y%m%d %H:%M:%S"),$9,$10}'`
sleep 2
done
