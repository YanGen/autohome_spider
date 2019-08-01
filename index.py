#coding=utf-8
import requests
import os
import time
from selenium import webdriver
import re
import json
import csv
from bs4 import BeautifulSoup
headers = {
    # 'cookie':'NTESSTUDYSI=0161b45653e441498273495b489eb65f; EDUWEBDEVICE=2c9b053d6a0c48f290d73caae1b2c2d4; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1557993916; __utma=63145271.211425529.1557993916.1557993916.1557993916.1; __utmc=63145271; __utmz=63145271.1557993916.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WM_NI=DuqV0b%2BkLlU9Ije8Fh6V9xYjx32sxRl7Xu5rrYyAoFIhlLVrcTBlR4KJnuQNUpw6wjMzw7i0vD5NuPMKmfDVvsVE0ATCyGVyKZSPL8fXg1OOk%2BV8zbnobLoW9khCQqDsbjY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7f87fb392ff87ce6da3928eb6c54b939b9b84ee638af5be9ad3508292a78cb52af0fea7c3b92a88abbfb7b36ae9b5848dd8338bb6abd9c564f68af799dc62bcedfe94fb5ab0e99896b87ab287b7a2ee4e8bb8a4add57aa18c8e8dd1408996a296d44697b0b9d7f6628fa6b9d8ec3cb69cfbaff85c8f95a387c75eb6ad9aa6b34b989db7a8d57389869db1cf34a688a9d2ce45a9f59ad9f96aaeb1aeadee5dfbb5a8a4d47b88adae8bdc37e2a3; WM_TID=4fkKYi6oQ9hBRBFBFEIsyN%2B73fXFN3g6; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1557995738; __utmb=63145271.19.9.1557995739845',
    # 'X-Requested-With':'XMLHttpRequest',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
if not os.path.exists("middle"):
    os.makedirs("middle")
reqNum = 0

colNum = 0
req = requests.session()
req.headers = headers

def retry(count=1):
    def dec(f):
        def ff(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    ans = f(*args, **kwargs)
                    return ans
                except Exception as e:
                    ex = e
            raise ex

        return ff

    return dec

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@retry(10)
def postApi(url,data):
    global req
    global reqNum
    reqNum +=1
    print("程序第",reqNum,"次请求~")
    # 请求模块执行POST请求,response为返回对象
    response = requests.post(url, data=data,headers = headers,timeout=5)
    # 从请求对象中拿到相应内容解码成utf-8 格式
    html = response.content.decode("utf-8")
    return html
@retry(10)
def loadPage(url,charSet=None,apiReq=False):
    global req
    global reqNum
    reqNum +=1
    print("程序第",reqNum,"次请求~")
    # 请求模块执行POST请求,response为返回对象
    response = req.get(url, headers = headers,timeout=10)
    headers['Referer'] = url
    # 从请求对象中拿到相应内容解码成utf-8 格式
    if charSet:
        html = response.content.decode(charSet)
    else:
        html = response.content.decode("utf-8")
    return html
@log("execute")
def fun():

    csvFile = open("ind.csv",newline="",mode="w",encoding="gbk")

    csvWriter = csv.writer(csvFile)

    cs = [chr(i) for i in range(ord("A"), ord("Z") + 1)]

    for c in cs:
        url= "https://www.autohome.com.cn/grade/carhtml/{}.html".format(c)
        html = loadPage(url,charSet="gbk")
        soup = BeautifulSoup(html,"html.parser")
        dlTags = soup.find_all("dl")
        for dlTag in dlTags:
            print("品牌名",dlTag.div.a.text)
            a = dlTag.div.a.text
            print("品牌ID",dlTag.div.a['href'].split(".html")[0].replace("//car.autohome.com.cn/price/brand-","").replace("//car.autohome.com.cn/pic/brand-",""))
            b = dlTag.div.a['href'].split(".html")[0].replace("//car.autohome.com.cn/price/brand-","").replace("//car.autohome.com.cn/pic/brand-","")
            ulTags = dlTag.find_all("ul")
            for ulTag in ulTags:
                result = re.compile('autohome\.com\.cn/(\d+)/#levelsource=000000000_0&amp;pvareaid=\d+">(.*?)</a>').findall(str(ulTag))
                for did ,name in result:
                    print("\t"+did,name)

                    dataList = [b,a,did,name]
                    dataList = [item.encode("gbk","ignore").decode("gbk") for item in dataList]
                    csvWriter.writerow(dataList)
    csvFile.close()

def Main():
    fun()



if __name__ == "__main__":
    Main()