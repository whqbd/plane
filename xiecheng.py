# -*- coding: utf-8 -*-

import requests,random,json ,re
import time
from user_agents import user_agents
key_word = "南京"
headers = {
    'cookie': '_RSG=YwKT_wrJIRFM1Lqbopb_78; _RDG=289992fa8b4bb024871183778bbc369e71; _RGUID=f6d24f5e-bf75-4ea2-81ff-973ca5d15056; _ga=GA1.2.590986197.1541752520; _abtest_userid=23eb24c9-08d2-4fe8-a12d-c9a9e1134c02; __utma=1.590986197.1541752520.1546589205.1546854996.2; __utmz=1.1546854996.2.2.utmcsr=ctrip.com|utmccn=(referral)|utmcmd=referral|utmcct=/; gad_city=b82f0154257a2ce862c5ae5da9f81b79; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _RF1=222.95.182.185; _gid=GA1.2.460034613.1552008640; MKT_Pagesource=PC; DomesticUserHostCity=NKG|%c4%cf%be%a9; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&Expires=1552635325422; MKT_OrderClick=ASID=4897155952&CT=1552030525423&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1541750405400.1kz65v"}; appFloatCnt=5; ASP.NET_SessionSvc=MTAuOC4xODkuNjZ8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTU1MTk1MzI0ODI2MA; _bfa=1.1541750405400.1kz65v.1.1552008636861.1552030522379.11.56; _bfs=1.5; _bfi=p1%3D600003794%26p2%3D600003794%26v1%3D56%26v2%3D55; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1552030679316%7D%5D; _jzqco=%7C%7C%7C%7C1552008639925%7C1.1084629649.1541752519768.1552030536166.1552030679360.1552030536166.1552030679360.undefined.0.0.51.51; __zpspc=9.12.1552030525.1552030679.4%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23',
    'origin': 'https://flights.ctrip.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': random.choice(user_agents),
    'content-type': 'application/json; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://flights.ctrip.com/fuzzy/',
    'authority': 'flights.ctrip.com',
    'x-requested-with': 'XMLHttpRequest',
}

#data = '{"inputDepartureCity":"SHA","inputDepartureCityName":"'+str(key_word.encode()).replace("b'",'').replace("\'",'').replace("\\","\\\\")+'","travelType":"ONEWAY","departStringDate":"\xe4\xbb\xbb\xe4\xbd\x95\xe6\x97\xb6\xe9\x97\xb4","departDateRanges":[],"maxDays":-1,"minDays":-1,"inputArrivalCities":{"themes":[],"cities":[],"areas":[]},"inputArrivalCitiesMap":{"themes":[],"cities":[],"areas":[],"filter":{}},"isSearchPage":true,"sortingType":"PRICE_ASC","isIncludedTax":true,"city_offset":480}'
data = '{"inputDepartureCity":"NKG","travelType":"ONEWAY","sortingType":"PRICE_ASC","isIncludedTax":true,"city_offset":480}'
response = requests.post('https://flights.ctrip.com/fuzzy/search', headers=headers, data=data)
print(response.text)
items = json.loads(response.text)["fuzzyFlightList"][0]["flightResultList"]
models = []
print(len(items))

for item in items:

    time.sleep(0.5)
    model = []
    model.append(key_word)
    model.append(item["aCityName"])
    #航班号
    # model.append(item["flightDetail"]["departFlightNo"])
    model.append(item["flightDetail"]["departDateString"])
    model.append(item["totalPrice"])
    model.append(item["discountRate"])
    model.append("携程网")
    print({"出发地":model[0],"目的地":model[1],"出发时间":model[2],"机票价格":model[3],"数据来源":model[5]})





    # print(json.loads(json.dumps(eval(str(item))))["flightDetail"]["departDateString"])


