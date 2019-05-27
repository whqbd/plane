#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/5/8 11:27
# @Author : whq
# @File : zh_carwl_bak.py

'''
反爬机制： 检测当前IP + 请求头 + cookie
    判断cookie：有过期时间, 过期后更新  self.AlteonP  self.sign_flight
    判断sessionid：sessionid过期 更新 整个cookies 或者 JSsessionid
    每请求一次  cookie中 PV值 加 1
'''
import requests, time, random, json,logging
from zh_city import zhCity

class ShenZhenAir:
    def __init__(self):

        self.url = 'http://www.shenzhenair.com/szair_B2C/flightSearch.action'

        # 日期的请求时添加  并且方便下一次更新调用
        self.form_data = {
            'condition.orgCityCode': 'NKG',
            'condition.dstCityCode': 'PEK',
            'condition.hcType': 'DC',
        }
        # referer 信息也在请求时添加，需要更新 post 传递参数，User-Agent不能修改，因为User-agent绑定cookie+IP

        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Length': '129',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.shenzhenair.com',
            'Origin': 'http://www.shenzhenair.com',
            'Proxy-Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        # cookie值 值取到 PV: 因为每次请求需要 加1 操作
        self.cookie = 'JSESSIONID=1022FCB800084F885501CDA1484DDF18; _gscu_1739384231=57134140sm720x62; _gscbrs_1739384231=1; AlteonP=BbE5XW9ADgp25w98sjKfDA$$; sign_cookie=35fc1f6966053f04e1391c6bd8e7f086; sign_flight=fbca866b032ea3fec1ae60051214d88e; CoreSessionId=f3f0534b902ace2e3f4b657f173d63c793948d9d8d763e54; _g_sign=269b38b2937bdfbcb17b6345b75ad5cf; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a955b00f53d7-0d55ecce95e296-5f1d3a17-2073600-16a955b00f6566%22%2C%22%24device_id%22%3A%2216a955b00f53d7-0d55ecce95e296-5f1d3a17-2073600-16a955b00f6566%22%7D; sajssdk_2015_cross_new_user=1; _dx_uzZo5y=d6818a349097655dd2d00073173542dc0d5e716deb68c7d61ea59153033f1abeb9061c29; fromPage=%7BfromPage%3A%22flightInit%22%7D; _gscs_1739384231=57283923a0s6aw18|pv:'

        # refer值 也需要拼接，所以只取到中间一部分 日期后面的部分在请求时拼接进去
        self.refer = 'http://www.shenzhenair.com/szair_B2C/flightsearch.action?orgCityCode=NKG&dstCityCode=PEK&orgDate='


    def getJson(self,start,end,date):
        # print(self.headers)
        n = 1
        p = 9
        n_time = time.localtime()
        base_time = int(time.strftime('%Y%m%d', n_time))
        try:
            while n<=1:
                # 时间更新用
                date = str(base_time)[0:4] + '-' + str(base_time)[4:6] + '-' + str(base_time)[6:]

                dstDate = base_time + 1
                conditiondstDate = str(dstDate)[0:4] + '-' + str(dstDate)[4:6] + '-' + str(dstDate)[6:]
                # 更新 传递的 data
                self.form_data['condition.orgDate'] = date
                self.form_data['condition.dstDate'] = conditiondstDate
                # 更新 请求头  信息
                self.headers['Referer'] = self.refer + date + '&hcType=DC'
                self.headers['Cookie'] = self.cookie + str(p)

                print('正在获取%s号信息' % date)
                # 发起请求获取数据
                res = requests.post(self.url, headers=self.headers, data=self.form_data)
                time.sleep(3)
                print("输出cookie")
                print(res.request.headers['Cookie'])
                print("输出cookie res.cookies")
                print(res.cookies)
                for c ,v in res.cookies.items():
                    print(c,v)
                # res.encoding = 'utf-8'
                print(res.text)
                html = json.loads(res.text)
                print('==' * 30)

                # 对获取的数据进行解析
                self.parseJson(html)
                #print(html)

                # 数值更新
                n += 1
                p += 1
                base_time += 1
                time.sleep(0.5)
        except json.decoder.JSONDecodeError:
            print('后续处理 or 没有航班')

    def parseJson(self, html):
        '''
        对获取的 Json数据进行解析
        :param html:
        :return:
        '''
        if len(html):
            info = html['flightSearchResult']['flightInfoList']
            for i in info:
                flightno = i['flightNo']
                orgdate = i['orgDate']
                orgtime = i['orgTime']
                dsttime = i['dstTime']
                orgcitych = i['orgCityCH']
                dstcitych = i['dstCityCH']

                print('去程: '+orgcitych +'-'+dstcitych + ' '+'机型: {}, 起飞日期: {}, 起飞时间: {}, 落地时间: {}'.format(flightno, orgdate, orgtime, dsttime))
                classinfolist = i['classInfoList']
                for j in classinfolist:
                    class_type = j['classCode']
                    class_price = j['classPrice']
                    print(class_type + '舱' + ': ' + class_price + '元')
                print()
            time.sleep(0.5)
        else:
            print('抱歉，该日期无座位或航班')

    def main(self):
        self.getJson()

if __name__ == '__main__':
    app = ShenZhenAir()
    app.main()
    # n_time = time.localtime()
    # base_time = int(time.strftime('%Y%m%d', n_time))
    # date = str(base_time)[0:4] + '-' + str(base_time)[4:6] + '-' + str(base_time)[6:]
    # print(date)