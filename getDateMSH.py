#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/22 10:52
# @Author : whq
# @File : getDateMSH.py

import datetime

#1起始时间 2 结束时间
def subtime(date1, date2):
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

    return date2 - date1

def getymdDate():
    nowdate = datetime.datetime.now()  # 获取当前时间
    d = nowdate.strftime("%Y%m%d")  # 当前时间转换为指定字符串格式
    return d



date1 = '2019-04-01 13:55:00'
date2 = '2019-04-01 11:40:00'

print(subtime(str(date1), str(date2)))  # date1 > date2
print(subtime(date2, date1))  # date1 < date2

nowdate = datetime.datetime.now()  # 获取当前时间
nowdate = nowdate.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间转换为指定字符串格式
print(subtime(date2, nowdate))  # nowdate > date2

if __name__ == '__main__':
    print(getymdDate())
    d = {}
    d.update({'bb':1})
    v = d.get('bb')

    if not v is None:
        print("v is not none",v)
    else:
        d.update({'aa':1})
    print(d)

