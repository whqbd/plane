#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/21 17:37
# @Author : whq
# @File : redisPy.py

import redis
import json
#redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

# r = redisPy.Redis(host='127.0.0.1', port=6379)

#ex 过期时间 单位秒
def setVal(key,val,ex=None):
    if not ex is None:
        r.set(key,val,ex)
    else:
        r.set(key,val)


def getVal(key):
    return r.get(key)

if __name__ == '__main__':
    paramstr = '{"data":[{"Airline":"中国国航","FlightNumber":"CA1120","DepartureDate":"09:00","ArrivalDate":"10:10","PunctualityRate":"67%","LowestPrice":250,"departureAirportInfo":"云冈机场","arrivalAirportInfo":"首都国际机场"}],"code":200,"msg":"success"}'
    setVal('test:whq:tickt',str,10)
    paramstr = getVal('flight:query:2019-04-01:DAT-BJS')
    print(paramstr)
    print(type(paramstr))

    d = eval(paramstr)
    print(type(d))
    print(d)
    print(json.dumps(d, ensure_ascii=False))
    print(paramstr)