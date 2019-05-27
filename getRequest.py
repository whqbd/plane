#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/14 17:46
# @Author : whq
# @File : getRequest.py
# 导入请求包request和将字典转换成bytes的包parse
from urllib import request, parse
# 导入请求失败时报错的包
from urllib.error import HTTPError, URLError
# 导入http中管理cookie的包
from http import cookiejar


# 将需要保存cookie的请求封装成类
class Session(object):
    def __init__(self):
        # 创建cookie容器对象，cookie_object
        cookie_object = cookiejar.CookieJar()
        # 创建cookie管理器，handler
        handler = request.HTTPCookieProcessor(cookie_object)
        # 新建一个带有cookie管理器的opener，替换原有的request.urlopen()
        # opener 遇到有cookie的response的时候,调用handler内部的一个函数, 存储到cookie object
        self.opener = request.build_opener(handler)

    # get请求
    def get(self, url, headers=None):
        return get(url, headers, self.opener)

    # post请求
    def post(self, url, form, headers=None):
        return post(url, form, headers, self.opener)


# 封装get请求
def get(url, headers=None, opener=None):
    return urlrequest(url, headers=headers, opener=opener)


# 封装post请求
def post(url, form, headers=None, opener=None):
    return urlrequest(url, form, headers=headers, opener=opener)


# 发送请求函数
def urlrequest(url, form=None, headers=None, opener=None):
    '''
    :param url: 访问地址
    :param form: post请求时发送的表单信息
    :param headers: 头信息
    :param opener: 带有cookie管理器的一个发送请求的东西
    :return: 返回响应信息的读取内容，response.read()
    '''

    # 如果没有传入headers，则使用下边默认headers
    if headers == None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
    # 当发生异常时返回空的二进制类型的html_bytes
    html_bytes = b''
    try:
        if form:  # POST请求
            # 转换成str
            form_str = parse.urlencode(form)
            # 转换成bytes
            form_bytes = form_str.encode('utf-8')
            # 传入post请求参数，form表单数据
            req = request.Request(url, data=form_bytes, headers=headers)
        else:  # GET请求
            req = request.Request(url, headers=headers)
            req.read

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    # 返回二进制响应结果
    return html_bytes


if __name__ == '__main__':
    # 百度测试get请求
    # url = 'http://www.baidu.com'
    # html_byte = get(url)
    # print(html_byte)
    # print('-'*50)
    # # 百度翻译测试post请求
    # url = 'http://fanyi.baidu.com/sug'
    # form = {
    #     'kw': '呵呵'
    # }
    # html_bytes = post(url, form=form)
    # print(html_bytes)
    url = "https://flights.ctrip.com/itinerary/api/12808/historyPunctuality"
    form ={'flightNo':'CZ3117'}
    # html_bytes = post(url, form=form)
    # print(html_bytes)
    res = request.Request(url,data=form)
    req = request.urlopen(res)
    respoen = req.read();
    result = str(respoen, encoding="utf-8")
    print(result)

