#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/5/8 16:39
# @Author : whq
# @File : testCookie.py
from selenium import webdriver
# from selenium.webdriver.chrome.optionsimport Options
#from selenium import webdriver driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

def get_cookie_from_network():

 # chrome_options = Options()
 # chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
 # chrome_options.add_argument('window-size=1920x3000')#指定浏览器分辨率
 # chrome_options.add_argument('--disable-gpu')#谷歌文档提到需要加上这个属性来规避bug
 # chrome_options.add_argument('--hide-scrollbars')#隐藏滚动条, 应对一些特殊页面
 # chrome_options.add_argument('blink-settings=imagesEnabled=false')#不加载图片, 提升速度
 # chrome_options.add_argument('--headless')#浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
 # chrome_options.binary_location =r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置
 #

 chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
 driver = webdriver.Chrome(chromedriver_path)

 url_login = 'http://www.shenzhenair.com/szair_B2C/toFlightSearch.action'
 # driver = webdriver.PhantomJS()
 #driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

 driver.get(url_login)

 # 获得 cookie信息
 cookie_list = driver.get_cookies()
 print (cookie_list)
if __name__ == '__main__':
 get_cookie_from_network()


