#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/27 9:23
# @Author : whq
# @File : crawl_xwzx.py
import requests ,random,json,re
import time
import hashlib
import datetime
import json
from user_agents import user_agents
from redis import *
from lxml import etree,html
from html.parser import HTMLParser
from redisPy import *

news_redis_key="news_redis_key:"
#新闻内容key
content_key = news_redis_key + "content:"
#新闻标题key
new_title_key = news_redis_key + "new:"


#去除标题中换行空格
def done(s):
        return str(s).replace("\n", '').strip()

def getZX():
    headers = {'user-agent': random.choice(user_agents)}
    url = 'http://www.caac.gov.cn/XWZX/'
    headers = {'user-agent': random.choice(user_agents)}
    response = requests.post(url,headers=headers)
    htmlstr = response.text
    doc = etree.HTML(htmlstr)
    #新闻详情url
    urls = doc.xpath("//div[@class='n_list']//ul/li/a/@href")
    #新闻标题
    titles = doc.xpath("//div[@class='n_list']//ul/li/a/text()")
    #新闻时间
    dates = doc.xpath("//div[@class='n_list']//ul/li/a/span/text()")

    # 去空格
    # lambda string: str(string).replace("\n", '').strip()
    titles =list(map(done,titles))
    #将数据组合成元祖
    data =zip(urls,titles,dates)
    print('>>>>>1',type(data))

    #len(data)
    #组装新闻数据 title date url
    news = []
    urlList=[]
    for itme in data:
        l = list(itme);
        urlstr = l[0]
        print(str(urlstr).find("XWZX"),urlstr)
        #只使用url中包含 XWZX的url地址 其他地址不要
        if str(urlstr).find("XWZX") > 0:
            print(">>>>1.1", urlstr)
            urlList.append(urlstr)
            obj = {}
            url = {}
            obj["title"] = l[1]
            obj["date"] = l[2]
            md5code=getmd5_val(l[0])
            # 将长url字符串 转32位md5 方便保存
            obj["val"] = md5code
            news.append(obj)

    print(">>2>>",news)
    print(">>2.1>>",urlList)


    #采集新闻详情 url news
    getNewDetails(urlList,news)


#根据url 获取新闻的详细内容
def getNewDetails(urls,data):

    exist_url=[]
    for u in urls:
        url = u
        md5code = getmd5_val(url)
        print(md5code, url)
        #1到redis查询是否已经存在页面
        obj = getVal(content_key+md5code)
        if not obj is None:
            #redis 取值不为空说明 url地址已经爬取过内容了 直接返回
            exist_url.append(md5code)
            print("页面已经采集过数据······")
            continue
        print("发现新数据,开始采集····")
        # 2对新数据进行采集
        headers = {'user-agent': random.choice(user_agents)}
        response = requests.get(url, headers=headers)
        htmlstr = response.text
       # print(html)
        tree = etree.HTML(htmlstr)
        content = tree.xpath("//div[@class='content']")
        print('xxx=',content[0])
        font = html.tostring(content[0])
        print(font)
        #html 转换为正常HTML代码
        decodefont = HTMLParser().unescape(font.decode())
        print (decodefont)
        #3数据保存redis
        setVal(content_key+md5code,decodefont)
        time.sleep(0.5)
    newDate =[];
    for d in data:
        val = d.get("val")
        if val not in exist_url:
            newDate.append(d)
    print(">>>>重复数据=", len(exist_url))
    print(">>>>新增数据=",len(newDate))


    #更新新闻数据
    if len(newDate):
        #更新原来的新闻信息先从redis取值，更新后存入

        data = getVal(new_title_key)
        if not data is None:
            datas = json.loads(data)
            print(">>>>>>>>旧数据长度>>>>",len(datas))
            print(">>>>3>>>",type(datas))
            newDate = list(datas)+newDate
            print(">>>>>>>>新数据长度>>>>",len(newDate))
            print(">>>>>>>>新数据长度内容1>>>>", newDate)

        print("新增数据2>>>",newDate)
        setVal(new_title_key, json.dumps(newDate,ensure_ascii=False))



#获取当前时间yyyymmdd
def getymdDate():
    nowdate = datetime.datetime.now()  # 获取当前时间
    d = nowdate.strftime("%Y%m%d")  # 当前时间转换为指定字符串格式
    return d


#获取字符串的md5密文SHA1与MD5都是摘要算法，且为不可逆算法
def getmd5_val(val):
    md = hashlib.md5()
    md.update(str(val).encode(encoding='utf-8'))
    return md.hexdigest()


if __name__ == '__main__':
    while True:
        getZX()
        time.sleep(180)#3小时跑一次 单位秒
