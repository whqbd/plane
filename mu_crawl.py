#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/5/9 17:51
# @Author : whq
# @File : mu_crawl.py
import requests
import json
from xc_city import city
from prettytable import PrettyTable

def donghang(dcity,acity,date):

    cookies = {
        '84bb15efa4e13721_gr_session_id': '7f53832d-ced8-4600-bb7e-265446c40668',
        '_ga': 'GA1.2.119121839.1557458048',
        '_gid': 'GA1.2.1558392222.1557458048',
        '_gat_UA-80008755-11': '1',
        'Webtrends': '707127db.5887ff62446d1',
        'language': 'zh_CN',
        'JSESSIONID': 'GiETBN+6DR5jDipD6RgXyG+O.laputaServer1',
        'gr_user_id': 'fd8bc616-3643-46e1-83c5-c0090ad021bd',
        '_gat': '1',
        'grwng_uid': '8fd57c9e-bfb7-4e02-a765-f1e2976d69ac',
        '84bb15efa4e13721_gr_session_id_7f53832d-ced8-4600-bb7e-265446c40668': 'true',
    }

    headers = {
        'Origin': 'http://www.ceair.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://www.ceair.com/booking/nkg-pek-190517_CNY.html',
        'X-Requested-With': 'XMLHttpRequest',
        'Proxy-Connection': 'keep-alive',
    }

    #deptCd  deptCityCode出发地 arrCd arrCityCode  arrCdTxt 目的地 deptCdTxt出发地 deptDt时间 2019-05-16
    ac = city.get(acity)
    dc = city.get(dcity)
    print('输入参数',acity,ac,dcity,dc)
    #date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
    if None == ac  or None == dc :
        return None
    if ac == 'BJS':
        ac = 'PEK'
    param = '{"deptCd":"'+dc+'","arrCd":"'+ac+'","deptDt":"'+date+'","deptAirport":"","arrAirport":"","deptCdTxt":"'+dcity+'","arrCdTxt":"'+acity+'","deptCityCode":"'+dc+'","arrCityCode":"'+ac+'"}'
    data = {
        '_': '684ccac0723f11e9ad95e7a3e738ddb2',
        'searchCond': '{"adtCount":1,"chdCount":0,"infCount":0,"currency":"CNY","tripType":"OW","recommend":false,"reselect":"","page":"0","sortType":"a","sortExec":"a","segmentList":['+param+'],"version":"A.1.0"}'
    }

    # dataparam = json.dumps(data)
    print('请求参数',data)
    rs = requests.post('http://www.ceair.com/otabooking/flight-search!doFlightSearch.shtml', headers=headers,
                       cookies=cookies, data=data)

    print('response 文本',rs.text)
    html = rs.content.decode('utf8')
    print('数据转码',html)
    jsonObj = json.loads(html)
    flightGroup = jsonObj['flightGroup']
    flightInfo = jsonObj['flightInfo']
    searchRoute = jsonObj['searchRoute']
    searchProduct = jsonObj['searchProduct']
    """
    1 lightGroup 获取直飞航班
    2 flightInfo 封装成 key index val obj
    3 searchRoute 封装成 dict
    4 searchProduct 封装成 key index val obj
    加载航班数据 根据flightGroup -> searchRoute[flightIndex]  获取对应价格表searchProduct  获取最低价格

    """
    if len(flightInfo) == 0:return None
    print(flightGroup)
    print(flightInfo)
    print(searchRoute)
    print(searchProduct)


    print(">>输出字典>>")
    # 1保存直飞航班index Group
    newFlightGroup = []
    for fg in flightGroup:
        if len(fg) == 1:
            newFlightGroup.append(fg)
    print(newFlightGroup)
    # 2处理航班数据封装成 dict
    newFlightInfo = {}
    for fi in flightInfo:
        newFlightInfo[str(fi['index'])] = fi
    print(newFlightInfo)
    # 3处理航班价格封装成dict,只要直飞的的数据不处理换乘数据
    newSearchRoute = {}
    for sr in searchRoute:
        flightIndex = sr['flightIndex']
        if len(flightIndex)==1:
            newSearchRoute[flightIndex[0]]=sr
    print(newSearchRoute)
    # 4 处理机票价格searchProduct 封装成 key index val obj 只保留index 和价格
    newSearchProduct = {}
    for sp in searchProduct:
        newSearchProduct[str(sp['index'])] = sp['salePrice']
    print(newSearchProduct)
    #保存组装好的数据
    dataList = []
    newFlightGroup.sort()
    print("获取直飞航班数据=", newFlightGroup)
    table = PrettyTable(["Airline", "FlightNumber", "DepartureDate", 'ArrivalDate', 'PunctualityRate', 'LowestPrice'
                            , 'departureAirportInfo', 'arrivalAirportInfo', 'craftTypeName', 'craftTypeKindDisplayName',
                         'mealType', 'date', 'rate'])
    for nfg in newFlightGroup:
        #航班基础信息
        flightInfo = newFlightInfo[nfg]
        #获取价格index对象
        searchRoute = newSearchRoute[nfg]
        #获取价格索引信息
        productIndexs = searchRoute['productIndex']
        salePrices = []
        for p in productIndexs:
            #在价格dict中取出对应价格
            salePrice = newSearchProduct[str(p)]
            salePrices.append(salePrice)
        #价格排序
        salePrices.sort()
        minPrice = salePrices[0]

        info = {}
        info['Airline'] = flightInfo['operatingAirline']['codeContext']
        info['FlightNumber'] = flightInfo['operatingAirline']['flightNumber']  # 飞机编号
        # 起飞时间
        dDate = flightInfo['departDateTime']
        # 到达时间
        aDate = flightInfo['arrivalDateTime']
        info['DepartureDate'] = dDate
        info['ArrivalDate'] = aDate
        info['PunctualityRate'] = ""
        info['LowestPrice'] = minPrice
        info['departureAirportInfo'] = flightInfo['departAirport']['codeContext']+flightInfo['departAirport']['terminal']
        info['arrivalAirportInfo'] = flightInfo['arrivalAirport']['codeContext']+flightInfo['departAirport']['terminal']
        info['craftTypeName'] = ""
        info['craftTypeKindDisplayName'] = ""
        info['mealType'] = ""
        info['date'] = flightInfo['duration']
        # 折扣价
        info['rate'] = ""
        dataList.append(info)
        table.add_row(info.values())

        print(nfg)
    print("东航航班数据》》")
    print(table)
    return dataList


if __name__ == '__main__':
    dcity = '南京'
    acity = '北京'
    date = '2019-06-17'

    resutl = donghang(dcity,acity,date)
    print(resutl)

