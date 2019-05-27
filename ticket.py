#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/14 17:42
# @Author : whq
# @File : ticket.py
import requests,random,json ,re
import time
import datetime
from prettytable import PrettyTable
from user_agents import user_agents
from xc_city import *
from redisPy import *
from mu_crawl import *

headers = {'user-agent': random.choice(user_agents)}
#统一redis失效时间
redis_ex = 6000

#获取航班历史准点记录 # date=日期 depDelay 延误时间 arrDelay=提前时间 -1
def getHistoryPunctuality(flightNo):
    headers = {'user-agent': random.choice(user_agents)}
    url = 'https://flights.ctrip.com/itinerary/api/12808/historyPunctuality'
    form = {'flightNo': flightNo}
    headers = {'user-agent': random.choice(user_agents)}
    response = requests.post(url,headers=headers,data=form)
    datajson = response.text
    obj = json.loads(datajson)
    return obj

#获取航班详细信息*需要参数 {出发地dcity，目的地acity，时间startDate，航班号flightNos}
def getFlightComfortableInfo(dcity,acity,startDate,flightNo):
    headers = {
        'user-agent':random.choice(user_agents),
        'Content-Type':'application/json',
        'Host': 'flights.ctrip.com',
        'Connection': 'keep-alive',
        'Origin': 'https://flights.ctrip.com',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',

    }
    url = 'https://flights.ctrip.com/itinerary/api/12808/flightComfortableInfo'
    form = '{"dcity":"'+dcity+'","acity":"'+acity+'","startDate":"'+startDate+'"}'
    #拼接参数先转成dict
    form = json.loads(form)
    #赋值数组
    form["flightNos"] = flightNo
    #转成接送字符串 变成最终请求参数
    form = json.dumps(form)
    print(form)
    response = requests.post(url, headers=headers, data=form)
    datajson = response.text
    # obj = json.loads(datajson)
    return datajson

#获取90天内最低票价直达最低票价
def get90DaysLowestPrice(dcity,acity):
    print("get 90day",dcity,acity)
    key = "90:"+getymdDate()+":"+dcity + "-" + acity
    dataJsonStr = getVal(key)
    # 判断redis数据不为None
    if not dataJsonStr is None:
        print(">>>>>>>>>>redis中数据还没过期>>>>>>>>>>>>>>>>>>data")
        print('redis get data....', dataJsonStr)
        return json.loads(dataJsonStr.decode("utf8"))

    url = 'https://flights.ctrip.com/itinerary/api/12808/lowestPrice'
    form = '{"dcity":"' + dcity + '","acity":"' + acity + '","flightWay":"Oneway","army":false}'
    headers = {'user-agent': random.choice(user_agents), 'Content-Type':'application/json'}
    response = requests.post(url, headers=headers,data=form)
    datajson = response.text

    oneWayPrice = json.loads(datajson)['data']
    print(oneWayPrice)
    print(type(oneWayPrice))
    dataJsonStr = json.dumps(oneWayPrice, ensure_ascii=False)
    setVal(key, dataJsonStr, redis_ex)
    return oneWayPrice

#根据输入的地名查找编码
def getPoicontent(key):
    url = 'https://flights.ctrip.com/itinerary/api/13076/getpoicontent?key='+key
    headers = {'user-agent': random.choice(user_agents), 'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    datajson = response.text
    #拼接参数先转成dict
    obj = json.loads(datajson)
    status = obj.get('status')
    if status == 0:
        data = obj.get('data')
    print(data)
    return datajson


def search(cityCode):
    url = 'https://flights.ctrip.com/fuzzy/search'
    form = '{"inputDepartureCity":"'+cityCode+'","inputDepartureCityName":"北京","travelType":"ONEWAY","departStringDate":"任何时间","departDateRanges":[],"maxDays":-1,"minDays":-1,"inputArrivalCities":{"themes":[],"cities":[],"areas":[]},"inputArrivalCitiesMap":{"themes":[],"cities":[],"areas":[],"filter":{}},"isSearchPage":true,"sortingType":"PRICE_ASC","isIncludedTax":true,"city_offset":480}'
    form = form.encode("utf-8")
    headers = {'user-agent': random.choice(user_agents),
               'content-type': 'application/json; charset=UTF-8',
               'accept': 'application/json, text/javascript, */*; q=0.01',
               }
    response = requests.post(url, headers=headers, data=form)
    datajson = response.text
    print(datajson)
    items = json.loads(datajson)["fuzzyFlightList"]
    dataList = []
    for it in items:
        fightResultList = it["flightResultList"]
        # print('2222.....', fightResultList)
        # print('3333type...', type(fightResultList))
        for res in fightResultList:
            # print(res)
            flightClass = res.get('flightClass')
            if flightClass == 'D' or flightClass == 'DI':
                # print(res)
                dataList.append(res)

            # acityName = res.get('aCityName','nano')
            # print(acityName)

    if len(dataList) >0:

        return json.dumps(dataList,ensure_ascii=False)
    # print(datajson)

#查询航班信息
def getProductsData(dcity, acity, date):
    cookies = {
        '_abtest_userid': 'a0b3ca4b-4e1c-47b7-9776-2ff7d7a3b374',
        '_RSG': '5BaD2ZMUARDojesz77jv58',
        '_RDG': '28b98accbd36f328e0110554c6e43d4555',
        '_RGUID': 'd6ca7968-c236-42c5-8179-b471fdda8b72',
        '_ga': 'GA1.2.1327874834.1552983784',
        '_gid': 'GA1.2.1906017295.1552983784',
        'MKT_Pagesource': 'PC',
        'DomesticUserHostCity': 'NKG|%c4%cf%be%a9',
        'appFloatCnt': '1',
        'Session': 'SmartLinkCode=U1501923&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh',
        'Union': 'OUID=&AllianceID=928435&SID=1501923&SourceID=&Expires=1553672458385',
        'MKT_OrderClick': 'ASID=9284351501923&CT=1553067658389&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3FAllianceID%3D928435%26sid%3D1501923%26ouid%3D%26app%3D0101F00&VAL={"pc_vid":"1552983781506.3xavyl"}',
        'gad_city': 'b82f0154257a2ce862c5ae5da9f81b79',
        'FD_SearchHistorty': '{"type":"S","data":"S%24%u9752%u5C9B%28TAO%29%24TAO%242019-03-30%24%u5317%u4EAC%28BJS%29%24BJS%24%24%24"}',
        '_bfa': '1.1552983781506.3xavyl.1.1553069857255.1553131682829.4.26',
        '_RF1': '222.95.180.150',
        'Mkt_UnionRecord': '%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1552987162512%7D%2C%7B%22aid%22%3A%22928435%22%2C%22timestamp%22%3A1553131684977%7D%5D',
        '_jzqco': '%7C%7C%7C%7C1553071415401%7C1.737548370.1552983784447.1553071507508.1553131684993.1553071507508.1553131684993.undefined.0.0.25.25',
        '__zpspc': '9.5.1553131685.1553131685.1%233%7Cwww.361way.com%7C%7C%7C%7C%23',
        '_bfi': 'p1%3D10320673302%26p2%3D10320673302%26v1%3D26%26v2%3D25',
    }

    headers = {
        'Origin': 'https://flights.ctrip.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': '*/*',
        'Referer': 'https://flights.ctrip.com/itinerary/oneway/dat-bjs?date=2019-04-02',
        'Connection': 'keep-alive',
    }

    ac = city.get(acity)
    dc = city.get(dcity)
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
    key = 'flight:query:' + date + ":" + city.get(dcity) + "-" + city.get(acity)
    dataJsonStr = getVal(key)
    # 判断redis数据不为None
    if not dataJsonStr is None:
        # result = eval(dataJsonStr)
        result = dataJsonStr.decode("utf8")
        result = json.loads(result)
        print(">>>>>>>>>>redis中数据还没过期>>>>>>>>>>>>>>>>>>data")
        #redis中的数据都是字符串的，读取出来就是字符串，通过eval就可以转出来了
        return json.dumps(result,ensure_ascii=False)
    print('redis get data....',dataJsonStr)

    dataparam = {"flightWay": "Oneway",
     "classType": "ALL",
     "hasChild": 'false',
     "hasBaby": 'false',
     "searchIndex": 1,
     "airportParams": [{"dcity": city.get(dcity), "acity": city.get(acity), "dcityname": dcity, "acityname": acity,
                        "date": date}]}
    dataparam = json.dumps(dataparam)
    param = dataparam.encode('utf-8')

    response = requests.post('https://flights.ctrip.com/itinerary/api/12808/products', headers=headers, cookies=cookies,
                             data=param).text
    # print(response)
    #判断状态码 == 0的时候有数据
    routeList = json.loads(response).get('data').get('routeList')
    table = PrettyTable(["Airline", "FlightNumber", "DepartureDate", 'ArrivalDate', 'PunctualityRate', 'LowestPrice'
                            ,'departureAirportInfo','arrivalAirportInfo','craftTypeName','craftTypeKindDisplayName','mealType','date','rate'])
    #保存数据集合
    dataList = []
    #统计航班数量
    filterNum = {}
    for route in routeList:
        if len(route.get('legs')) == 1:
            info = {}
            ft = {}
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            #统计航班数量
            f_num =filterNum.get(flight.get('airlineName'))
            if not f_num is None:
                filterNum.update({flight.get('airlineName'):f_num+1})
            else:
                filterNum.update({flight.get('airlineName'):1})
            info['Airline'] = flight.get('airlineName')
            info['FlightNumber'] = flight.get('flightNumber')
            #起飞时间
            dDate = flight.get('departureDate')
            #到达时间
            aDate = flight.get('arrivalDate')
            info['DepartureDate'] = flight.get('departureDate')[-8:-3]
            info['ArrivalDate'] = flight.get('arrivalDate')[-8:-3]
            info['PunctualityRate'] = flight.get('punctualityRate')
            info['LowestPrice'] = legs.get('characteristic').get('lowestPrice')
            info['departureAirportInfo'] = flight.get('departureAirportInfo').get('airportName')
            info['arrivalAirportInfo'] = flight.get('arrivalAirportInfo').get('airportName')
            info['craftTypeName'] = flight.get('craftTypeName')
            info['craftTypeKindDisplayName'] = flight.get('craftTypeKindDisplayName')
            info['mealType'] = flight.get('mealType')
            info['date'] = str(subtime(str(dDate), str(aDate)))
            #折扣价
            info['rate'] = legs.get('cabins')[0].get('price').get('rate')
            dataList.append(info)
            table.add_row(info.values())
    #将有效数据转json字符串返回

    # 查询东航数据
    donghangJson = None
    try:
        donghangJson = donghang(dcity, acity, date)
    except Exception as e:
        print('搜索东航数据出现异常=>',str(e))

    dataObj = {}
    dataObj.update({"flight":dataList})
    dataObj.update({"flightNum":filterNum})
    dataObj.update({"muFlight":donghangJson})
    dataJsonStr = json.dumps(dataObj, ensure_ascii=False)
    setVal(key,dataJsonStr,redis_ex) #redis 保存5分钟
    print("航班数量》》》",filterNum)
    print(dcity, '------->', acity)
    print(table)
    return str(dataJsonStr)


# 定义通用返回json字符串格式
def jsonResult(data=None, code=200, msg='success'):
    result = {}
    result.update({'data': data})
    result.update({'code': code})
    result.update({'msg': msg})
    return json.dumps(result,ensure_ascii=False)


#计算两个时间差1起始时间 2 结束时间
def subtime(date1, date2):
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

    return date2 - date1
#获取当前时间yyyymmdd
def getymdDate():
    nowdate = datetime.datetime.now()  # 获取当前时间
    d = nowdate.strftime("%Y%m%d")  # 当前时间转换为指定字符串格式
    return d


#90天最低价排序返回最低前10个日期
def sort_by_LowestPrice(dictDate):
    #按价格值排序 {"20190325": 410, "20190326": 530,}
    aa = dict(sorted(dictDate.items(), key=lambda d: d[1]))
    print(aa)
    #取出最低价前10个
    bb = {}
    i = 1
    for n, v in aa.items():
        bb.update({n: v})
        if i == 10:
            break
        i = i + 1
    print(bb)
    #将10个数据按日期重排序
    cc = dict(sorted(bb.items(), key=lambda d: d[0]))
    print(cc)
    return cc



if __name__ == '__main__':
    ##获取航班历史准点记录
    # no = 'MU5137'
    # obj = getHistoryPunctuality(no);
    # items = obj['data']
    # # date=日期 depDelay 延误时间 arrDelay=提前时间 -1
    # for it in items:
    #     print(it['date'], it['depDelay'], it['arrDelay'])
    #------------------------------------------------------
    #获取航班详细信息
    # dcity = "BJS"
    # acity = "NKG"
    # startDate = "2019-04-01 09:00:00"
    # flightNo = ["CA1817"]
    # obj = getFlightComfortableInfo(dcity,acity,startDate,flightNo)
    # print(obj)
    #-----------------------------------------------------
    #90天内最低票价直达最低票价
    # dcity = 'CGO'
    # acity = 'CSX'
    # obj = get90DaysLowestPrice(dcity,acity)
    # print(obj)
    #------------------------------------
    #根据关键字查地名code
    # key = "nj"
    # obj = getPoicontent(key)
    # print(obj)
    #----------------------------
    # 查询地区折扣票价
    # cityCode = 'WUH'
    # json = search(cityCode)
    # print (json)
    #----------------------------------
    #查询航班
    # dcity = '大同'
    # acity = '南京'
    # date = '20190401'
    # # xiecheng(dcity, acity, date)
    # getProductsData(dcity, acity, date)
    #---------------------------
    liststr=[{'title': 'aaa', 'date': '2019-03-28'}
        ,{'title': 'bbb', 'date': '2019-03-27'}
        ,{'title': 'ee', 'date': '2019-03-29'}
        , {'title': 'ff', 'date': '2019-03-25'}
        , {'title': 'gg', 'date': '2019-03-29'}
             ]
    print(sorted(liststr, key=lambda x: x['date']))




