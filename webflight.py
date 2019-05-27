#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/18 15:27
# @Author : whq
# @File : webflight.py
from flask import Flask,render_template,request
from flask_cors import *  # 导入模块
from ticket import *
from xc_city import *
from mu_crawl import *

import json

app = Flask(__name__,static_url_path='/static/',template_folder='templates')
api='/api'
CORS(app, supports_credentials=True)  # 设置跨域

#获取首页热门
@app.route(api + '/home', methods=['GET', 'POST'])
def home():
    ip = request.remote_addr
    print(">>>>",ip)
    cityCode = request.form.get("cityCode") or "NO"
    if cityCode == 'NO':
        cityCode = 'WUH'
    jsonStr = search(cityCode)
    jsonStr = json.loads(jsonStr)
    print(type(jsonStr))
    result = {}
    result.update({'data': jsonStr})
    result.update({'code': 200})
    result.update({'msg': 'success'})
    return json.dumps(result, ensure_ascii=False), {"Content-Type": "application/json"}


# 查询获取航班
@app.route(api + '/price', methods=['GET', 'POST'])
def price():
    dcity = request.form.get("dcity") or "NO"
    acity = request.form.get("acity") or "NO"
    date = request.form.get("date") or "NO"
    if dcity == 'NO' or acity == 'NO' or acity == 'NO':
        return jsonResult(code=500, msg='参数错误')
    jsonDataStr = getProductsData(dcity, acity, date)

    print(jsonDataStr)
    jsonDataStr = json.loads(str(jsonDataStr))
    return jsonResult(data=jsonDataStr, msg='success'), {"Content-Type": "application/json"}

#获取90价格 返回最低价10条数据
@app.route(api + '/get90DaysLowestPrice', methods=['GET', 'POST'])
def get90DaysPrice():
    dcity = request.form.get("dcity") or "NO"
    acity = request.form.get("acity") or "NO"

    if dcity == 'NO' or acity == 'NO':
        return jsonResult(code=500, msg='参数错误')
    ac = city.get(acity)
    dc = city.get(dcity)
    obj = get90DaysLowestPrice(dc, ac)
    print(type(obj))
    """对 90内优惠机票排序 显示最低价10条信息"""
    one = obj.get('oneWayPrice')
    print(one)
    print("90天排序数据》》",one[0])
    # oneWay = dict(sorted(one[0].items(), key=lambda d: d[1]))
    oneWay = sort_by_LowestPrice(one[0])
    print("90天排序后数据》》",oneWay)
    obj.update({'oneWayPrice': oneWay})
    print(obj)
    # =====================end=====
    result = {}
    result.update({'data': obj})
    result.update({'code': 200})
    result.update({'msg': 'success'})
    return json.dumps(result, ensure_ascii=False), {"Content-Type": "application/json"}


# 获取航班准点率
@app.route(api + '/getHistoryPunctuality', methods=['GET', 'POST'])
def HistoryPunctuality():
    flightNo = request.form.get("flightNo") or "NO"
    if flightNo == 'NO':
        return jsonResult(code=500, msg='参数错误')
    data = getHistoryPunctuality(flightNo)

    dates = []
    depDelay = []
    arrDelay = []

    items = data['data']
    # date=日期 depDelay 延误时间 arrDelay=提前时间 -1
    for it in items:
        print(it['date'], it['depDelay'], it['arrDelay'])
        dates.append(it['date'])
        d = it['depDelay'] if not it['depDelay'] is None else 0
        a = it['arrDelay'] if not it['arrDelay'] is None else 0
        depDelay.append(d)
        arrDelay.append(a)

    print(dates)
    print(depDelay)
    print(arrDelay)
    resultData = {}
    resultData.update({"dates": dates})
    resultData.update({"depDelay": depDelay})
    resultData.update({"arrDelay": arrDelay})

    result = {}
    result.update({'data': resultData})
    result.update({'code': 200})
    result.update({'msg': 'success'})
    return jsonResult(data=result, msg='success'), {"Content-Type": "application/json"}


# 获取航班具体信息
@app.route(api+"/getFlightComfortableInfo",methods=['GET', 'POST'])
def findFlightComfortableInfo():
    dcitystr = request.form.get("dcity") or "NO"
    acitystr = request.form.get("acity") or "NO"
    date = request.form.get("date") or "NO"
    tm = request.form.get("time") or "NO"
    flightNo = request.form.get("flightNo") or "NO"
    if dcitystr == 'NO' or acitystr == 'NO' or date == 'NO' or flightNo =='NO':
        return jsonResult(code=500, msg='参数错误')
    acity = city.get(acitystr)
    dcity = city.get(dcitystr)
    startDate = date[0:4] + '-' + date[4:6] + '-' + date[6:8]+' '+tm+':00'
    flight_nos = []
    flight_nos.append(flightNo)
    #flight_nos = json.dumps(flight_nos)
    print(acity,dcity,date,tm,flight_nos)
    # startDate = "2019-04-01 19:05:00"
    # flightNo = ["CA8209", "CA8207"]
    obj = getFlightComfortableInfo(dcity, acity, startDate, flight_nos)
    print(obj)
    jsonObj= json.loads(obj)
    resultData=jsonObj.get("data")
    print("resultData....",resultData)

    # json.dumps(字典)  # 将python的字典转换为json字符串
    # json.loads(字符串)  # 将json字符串转换为python字典

    return jsonResult(data=resultData, msg='success'), {"Content-Type": "application/json"}


news_redis_key="news_redis_key:"
#新闻内容key
content_key = news_redis_key + "content:"
#新闻标题key
new_title_key = news_redis_key + "new:"
@app.route(api+"/getNewsList",methods=['GET', 'POST'])
def getNewsList():
    news = getVal(new_title_key)
    news = news.decode("utf8")
    jsonObj = json.loads(news)
    print(" 原始数据>>", jsonObj)
    aa = sorted(jsonObj, key=lambda x: x['date'],reverse=True)
    print(" 按日排序数据>>", aa)

    return jsonResult(data=aa, msg='success'), {"Content-Type": "application/json"}


@app.route(api + "/getNewsDetail", methods=['GET', 'POST'])
def getNewsDetail():
    val = request.form.get("val") or "NO"
    if val == 'NO':
        return jsonResult(code=500, msg='参数错误')

    news = getVal(content_key + val)
    news = news.decode("utf8")
    print(news)
    # jsonObj = json.loads(news)

    return jsonResult(data=news, msg='success'), {"Content-Type": "application/json"}



if __name__ == '__main__':
    app.run(
        #host='0.0.0.0',
        port=8800,
        debug=True
    )
