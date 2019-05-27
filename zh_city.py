#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/5/7 9:43
# @Author : whq
# @File : sh_city.py

import requests,random,json ,re
import datetime
from user_agents import user_agents

zhCity={'迪庆': 'DIG', '东营': 'DOY', '大连': 'DLC', '大理': 'DLU', '丹东': 'DDG', '稻城': 'DCY', '大庆': 'DQA', '大同': 'DAT',
        '达州': 'DAX', '敦煌': 'DNH', '恩施': 'ENH', '鄂尔多斯': 'DSN', '佛山': 'FUO', '抚远': 'FYJ', '富蕴': 'FYN', '福州': 'FOC',
        '阜阳': 'FUG', '广州': 'CAN', '格尔木': 'GOQ', '广汉': 'GHN', '贵阳': 'KWE', '桂林': 'KWL', '赣州': 'KOW', '广元': 'GYS',
        '安康': 'AKA', '安庆': 'AQG', '安顺': 'AVA', '阿坝': 'AHJ', '阿勒泰': 'AAT', '阿克苏': 'AKU', '北京': 'PEK', '百色': 'AEB',
        '保山': 'BSD', '毕节': 'BFJ', '布尔津': 'KJI', '巴中': 'BZX', '包头': 'BAV', '巴彦淖尔': 'RLK', '北海': 'BHY', '成都': 'CTU',
        '重庆': 'CKG', '长春': 'CGQ', '常德': 'CGD', '长沙': 'CSX', '长白山': 'NBS', '昌都': 'BPX', '长治': 'CIH', '常州': 'CZX',
        '朝阳': 'CHG', '赤峰': 'CIF', '池州': 'JUH', '黎平': 'HZH', '连云港': 'LYG', '荔波': 'LLB', '临汾': 'LFQ', '龙岩': 'LCX',
        '洛阳': 'LYA', '临沧': 'LNJ', '兰州': 'LHW', '丽江': 'LJG', '临沂': 'LYI', '林芝': 'LZY', '六盘山': 'GYU', '六盘水': 'LPF',
        '柳州': 'LZH', '泸州': 'LZO', '漠河': 'OHE', '梅县': 'MXZ', '绵阳': 'MIG', '芒市': 'LUM', '满洲里': 'NZH', '牡丹江': 'MDG',
        '南京': 'NKG', '南昌': 'KHN', '南宁': 'NNG', '南阳': 'NNY', '那拉提': 'NLT', '宁波': 'NGB', '南通': 'NTG', '南充': 'NAO',
        '海口': 'HAK', '哈尔滨': 'HRB', '合肥': 'HFE', '汉中': 'HZG', '黑河': 'HEK', '衡阳': 'HNY', '杭州': 'HGH', '惠州': 'HUZ',
        '呼和浩特': 'HET', '黄岩': 'HYN', '淮安': 'HIA', '河池': 'HCJ', '怀化': 'HJJ', '海拉尔': 'HLD', '哈密': 'HMI', '邯郸': 'HDG',
        '和田': 'HTN', '黄山': 'TXN', '吉安': 'KNC', '建三江': 'JSJ', '嘉峪关': 'JGN', '吉林': 'JIL', '锦州': 'JNZ', '九江': 'JIU',
        '济南': 'TNA', '景德镇': 'JDZ', '佳木斯': 'JMU', '揭阳': 'SWA', '井冈山': 'JGS', '景洪': 'JHG', '济宁': 'JNG', '九寨沟': 'JZH',
        '鸡西': 'JXA', '昆明': 'KMG', '康定': 'KGT', '库车': 'KCA', '克拉玛依': 'KRY', '喀什': 'KHG', '库尔勒': 'KRL', '天水': 'THQ',
        '塔城': 'TCG', '吐鲁番': 'TLQ', '太原': 'TYN', '天津': 'TSN', '铜仁': 'TEN', '台州': 'HYN', '腾冲': 'TCZ', '通化': 'TNH',
        '通辽': 'TGO', '无锡': 'WUX', '五大连池': 'DTU', '潍坊': 'WEF', '芜湖': 'WHU', '梧州': 'WUZ', '文山': 'WNH', '乌兰察布': 'UCB',
        '温州': 'WNZ', '乌鲁木齐': 'URC', '武汉': 'WUH', '万州': 'WXN', '威海': 'WEH', '乌海': 'WUA', '乌兰浩特': 'HLH', '武夷山': 'WUS',
        '泉州': 'JJN', '黔江': 'JIQ', '且末': 'IQM', '庆阳': 'IQN', '青岛': 'TAO', '琼海': 'BAR', '秦皇岛': 'SHP', '齐齐哈尔': 'NDG',
        '衢州': 'JUZ', '攀枝花': 'PZI', '深圳': 'SZX', '沈阳': 'SHE', '沙市': 'SHS', '石河子': 'SHF', '狮泉河': 'NGQ', '十堰': 'WDS',
        '思茅': 'SYM', '松原': 'YSQ', '苏州': 'SZV', '上海虹桥': 'SHA', '上海浦东': 'PVG', '三亚': 'SYX', '邵阳': 'WGN', '汕头': 'SWA',
        '石家庄': 'SJW', '日照': 'RIZ', '日喀则': 'RKZ', '永州': 'LLF', '伊尔施': 'YIE', '玉树': 'YUS', '宜昌': 'YIH', '银川': 'INC',
        '扬州': 'YTY', '烟台': 'YNT', '延安': 'ENY', '盐城': 'YNZ', '延吉': 'YNJ', '宜宾': 'YBP', '宜春': 'YIC', '伊宁': 'YIN',
        '义乌': 'YIW', '榆林': 'UYN', '运城': 'YCU', '西安': 'XIY', '邢台': 'XNT', '兴义': 'ACX', '厦门': 'XMN', '襄阳': 'XFN',
        '西宁': 'XNN', '西昌': 'XIC', '锡林浩特': 'XIL', '忻州': 'WUT', '徐州': 'XUZ', '郑州': 'CGO', '中卫': 'ZHY', '珠海': 'ZUH',
        '舟山': 'HSN', '张家界': 'DYG', '湛江': 'ZHA', '昭通': 'ZAT', '遵义茅台': 'WMT'}

#获取地址使用
def getCity():

    url = 'http://www.shenzhenair.com/szair_B2C/getCitys.action?plat=B2C'
    headers = {'user-agent': random.choice(user_agents)}
    response = requests.get(url,headers=headers)
    datajson = response.json()
    print('response type?',type(datajson))
    print(datajson)
    internalCityMap = datajson['cityDto']['internalCityMap']
    print(internalCityMap)
    newCity = {}
    for k in internalCityMap:
        city = internalCityMap[k]
        for c in city:
            newCity[c.get('fullName')] = c.get('shortName')

            # print(c.get('fullName'),c.get('shortName'))
    print(newCity)
def getData(orgCity,dstCity,orgDate,pv):

    orgCityCode = zhCity.get(orgCity)
    dstCityCode = zhCity.get(dstCity)

    if None is orgCityCode or None is dstCityCode:
        print('航班地址不存在')
        return None
    """ userAgent  和 cookies 需要手动从浏览器中获得 深航反爬验证这两个比较严格 """
    userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

    cookies = 'JSESSIONID=81624CA91443D2FC12F0DABC59474B7A; AlteonP=BHHNIW9ADgrAzf4I9fTgHw$$; sign_cookie=2188a976026ae2a130d2551c8a3789c9; sign_flight=49cd1666b6e259754aee062dbbd94a3d; CoreSessionId=05951efdc0cb8f13c01aa27a81e5b88e8194967384ccc3e3; _g_sign=f0c6b3ccb4e5750b1771888b4874ae67; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a9a3a27e02ad-0d449ccc69ed6d-5f1d3a17-2073600-16a9a3a27e16bd%22%2C%22%24device_id%22%3A%2216a9a3a27e02ad-0d449ccc69ed6d-5f1d3a17-2073600-16a9a3a27e16bd%22%7D; sajssdk_2015_cross_new_user=1; _gscu_1739384231=57134140sm720x62; _gscbrs_1739384231=1; _dx_uzZo5y=d6818a349097655dd2d00073173542dc0d5e716deb68c7d61ea59153033f1abeb9061c29; fromPage=%7BfromPage%3A%22flightInit%22%7D; _gscs_1739384231=57365663ewskcv13|pv:'

    url = 'http://www.shenzhenair.com/szair_B2C/flightSearch.action'
    #cookie中 pv 值验证网址访问次数 比较有用，cookie中的值开始算起 每次请求PV+1
    pv = pv
    orgDate = int(orgDate)
    date = str(orgDate)[0:4] + '-' + str(orgDate)[4:6] + '-' + str(orgDate)[6:]
    orgDate +=1
    conditiondstDate = str(orgDate)[0:4] + '-' + str(orgDate)[4:6] + '-' + str(orgDate)[6:]

    #也很关键
    refer = 'http://www.shenzhenair.com/szair_B2C/flightsearch.action?orgCityCode='+orgCityCode+'&dstCityCode='+dstCityCode+'&orgDate='+date+'&hcType=DC'


    headers = {
        'Origin': 'http://www.shenzhenair.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Proxy-Connection': 'keep-alive',
    }

    headers['Referer'] = refer
    headers['Cookie'] = cookies + str(pv)
    headers['User-Agent'] = userAgent


    data = {
        'condition.orgCityCode':orgCityCode,
        'condition.dstCityCode': dstCityCode,
        'condition.hcType': 'DC',
        'condition.orgDate': date,
        'condition.dstDate': conditiondstDate,

    }

    print(headers)
    print(data)

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
    html = ""
    try:
        html = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print('cookie过期后续处理 or 没有航班')
        return "没有数据"
    print(html)
    #parseJson(jsonData)

    dataList = []
    if len(html):
        info = html['flightSearchResult']['flightInfoList']
        for i in info:
            flightno = i['flightNo']
            orgdate = i['orgDate']#起飞日期
            orgtime = i['orgTime']#起飞时间
            dsttime = i['dstTime']#落地时间
            orgcitych = i['orgCityCH'] #出发地
            dstcitych = i['dstCityCH'] #目的地
            carrier = i['carrier']
            carrierFlightNo = i['carrierFlightNo']

            print('去程: ' + orgcitych + '-' + dstcitych + ' ' + '机型: {}, 起飞日期: {}, 起飞时间: {}, 落地时间: {}'.format(flightno,
                                                                                                             orgdate,
                                                                                                             orgtime,
                                                                                                             dsttime))
            #计算出最低价格
            lastPrice = 0
            classinfolist = i['classInfoList']
            for j in classinfolist:
                class_type = j['classCode']
                class_price = j['classPrice']
                if lastPrice==0:
                    lastPrice = j['classPrice']
                else:
                    if int(class_price) < int(lastPrice):
                        lastPrice = class_price

                print(class_type + '舱' + ': ' + class_price + '元')
            print()

            info ={}
            info['Airline'] = carrier
            info['FlightNumber'] = i['flightNo'] #飞机编号
            # 起飞时间
            dDate = orgtime
            # 到达时间
            aDate = dsttime
            info['DepartureDate'] = orgtime
            info['ArrivalDate'] = dsttime
            info['PunctualityRate'] = ""
            info['LowestPrice'] = lastPrice
            info['departureAirportInfo'] =i['orgAirport']
            info['arrivalAirportInfo'] = i['dstAirport']
            info['craftTypeName'] = ""
            info['craftTypeKindDisplayName'] =""
            info['mealType'] = ""
            info['date'] = str(subtime(str(dDate), str(aDate)))
            # 折扣价
            info['rate'] = ""
            dataList.append(info)

        print('data>>>',dataList)
    else:
        print('抱歉，该日期无座位或航班')

    return dataList


#计算两个时间差1起始时间 2 结束时间
def subtime(date1, date2):
    date1 = datetime.datetime.strptime(date1, "%H:%M")
    date2 = datetime.datetime.strptime(date2, "%H:%M")

    return date2 - date1

if __name__ == '__main__':
    #getCity()
    #getData()

    orgDate = '20190510'
    rs = getData('南京','深圳',orgDate,5)
    print(rs)

