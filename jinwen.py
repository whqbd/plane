#中国禁闻网

url = "https://www.bannedbook.org/bnews/renquan/xizang/"
from  spiders.headers import headers
import requests
html =requests.get(str(url),headers=headers).text
from lxml import etree
doc = etree.HTML(html)
url =doc.xpath("//a[@class = 'posts-item-title-link']//@href")
for i  in url:
    print("https://xizang-zhiye.org"+str(i))