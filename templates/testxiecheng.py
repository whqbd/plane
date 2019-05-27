#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/21 9:25
# @Author : whq
# @File : testxiecheng.py

from prettytable import PrettyTable
import requests
import json

def xiecheng(dcity, acity, date):
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]

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
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Referer': 'https://flights.ctrip.com/itinerary/oneway/dat-bjs?date=2019-04-02',
        'Connection': 'keep-alive',
    }

    city = {'阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'MFM',
            '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
            '北京': 'BJS', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
            '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
            '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
            '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
            '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
            '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
            '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
            '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
            '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
            '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU', '九寨沟': 'JZH', '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
            '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
            '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
            '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
            '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
            '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
            '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
            '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
            '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
            '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
            '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL',
            '香格里拉(迪庆)': 'DIG',
            '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY', '延吉': 'YNJ', '盐城': 'YNZ',
            '伊春': 'LDS',
            '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF', '榆林': 'UYN',
            '玉树': 'YUS',
            '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO', '中卫': 'ZHY',
            '舟山': 'HSN',
            '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}


    url = 'https://flights.ctrip.com/itinerary/api/12808/products'
    request_payload = {"flightWay": "Oneway",
                       "classType": "ALL",
                       "hasChild": 'false',
                       "hasBaby": 'false',
                       "searchIndex": 1,
                       "airportParams": [
                           {"dcity": city.get(dcity), "acity": city.get(acity), "dcityname": dcity, "acityname": acity,
                            "date": date}]}

    # param = '{"flightWay":"Oneway","classType":"ALL","hasChild":false,"hasBaby":false,"searchIndex":1,"airportParams":[{"dcity":"dat","acity":"bjs","dcityname":"大同","acityname":"北京","date":"2019-04-02"}],"params":[{"dcity":"DAT","acity":"BJS","dcityname":"大同","acityname":"北京","date":"2019-04-01","dcityid":136,"acityid":12,"aport":"","aportname":""}],"army":false}'
    # param = param.encode('utf-8')
    # 这里传进去的参数必须为 json 格式
    # response = requests.post(url, data=param, headers=headers).text

    data = '${"flightWay":"Oneway","classType":"ALL","hasChild":false,"hasBaby":false,"searchIndex":1,"airportParams":[{"dcity":"dat","acity":"bjs","dcityname":"\\u5927\\u540c","acityname":"\\u5317\\u4eac","date":"2019-04-02"}],"params":[{"dcity":"dat","acity":"bjs","dcityname":"\\u5927\\u540c","acityname":"\\u5317\\u4eac","date":"2019-04-02"}],"army":false}'

    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    print (response.text)
    routeList = json.loads(response).get('data').get('routeList')
    table = PrettyTable(["Airline", "FlightNumber", "DepartureDate", 'ArrivalDate', 'PunctualityRate', 'LowestPrice'])

    for route in routeList:
        if len(route.get('legs')) == 1:
            info = {}
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            info['Airline'] = flight.get('airlineName')
            info['FlightNumber'] = flight.get('flightNumber')
            info['DepartureDate'] = flight.get('departureDate')[-8:-3]
            info['ArrivalDate'] = flight.get('arrivalDate')[-8:-3]
            info['PunctualityRate'] = flight.get('punctualityRate')
            info['LowestPrice'] = legs.get('characteristic').get('lowestPrice')

            table.add_row(info.values())

    print(dcity, '------->', acity, date)
    print(table)


#--------------------------


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

    city = {'阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'MFM',
            '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
            '北京': 'BJS', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
            '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
            '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
            '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
            '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
            '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
            '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
            '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
            '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
            '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU', '九寨沟': 'JZH', '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
            '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
            '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
            '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
            '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
            '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
            '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
            '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
            '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
            '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
            '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL',
            '香格里拉(迪庆)': 'DIG',
            '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY', '延吉': 'YNJ', '盐城': 'YNZ',
            '伊春': 'LDS',
            '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF', '榆林': 'UYN',
            '玉树': 'YUS',
            '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO', '中卫': 'ZHY',
            '舟山': 'HSN',
            '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}


    ac = city.get(acity)
    dc = city.get(dcity)
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
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
    table = PrettyTable(["Airline", "FlightNumber", "DepartureDate", 'ArrivalDate', 'PunctualityRate', 'LowestPrice','departureAirportInfo','arrivalAirportInfo'])
    #保存数据集合
    dataList = []
    for route in routeList:
        if len(route.get('legs')) == 1:
            info = {}
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            info['Airline'] = flight.get('airlineName')
            info['FlightNumber'] = flight.get('flightNumber')
            info['DepartureDate'] = flight.get('departureDate')[-8:-3]
            info['ArrivalDate'] = flight.get('arrivalDate')[-8:-3]
            info['PunctualityRate'] = flight.get('punctualityRate')
            info['LowestPrice'] = legs.get('characteristic').get('lowestPrice')
            info['departureAirportInfo'] = flight.get('departureAirportInfo').get('airportName')
            info['arrivalAirportInfo'] = flight.get('arrivalAirportInfo').get('airportName')
            dataList.append(info)
            table.add_row(info.values())
    #将有效数据转json字符串返回
    dataJsonStr = json.dumps(dataList)
    print(dataJsonStr)
    print(dcity, '------->', acity)
    print(table)
    return dataJsonStr


if __name__ == "__main__":
    # dcity = input('请输入起点： ')
    # acity = input('请输入终点： ')
    # date = input('请输入出行日期： ')
    #{"status":2,"msg":{"Message":"请求参数缺失","ErrorCode":"3000","StackTrace":null,"SeverityCode":null,"ErrorFields":null,"ErrorClassification":null},"transactionId":"756fe161FDOX48de9e5efcfbcda7f3d3"}
    dcity = '上海'
    acity = '北京'
    date = '20190401'
    # xiecheng(dcity, acity, date)
    getProductsData(dcity, acity, date)

