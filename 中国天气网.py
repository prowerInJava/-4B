#！/usr/bin/env python3
#chmod 777 xxxx.py
import json
class getCityCode():
      def __init__(self,path,city):
            self.path = path
            self.city = city
      def getCode(self):
            with open (self.path,'r',1,'gbk') as file:
                  data = json.load(file)
                  for i in range (len(data)):
                        if self.city in (data[i].values()):
                        #if data[i]['cityName'] == self.city:
                              self.cityCode = data[i]['cityCode']
            return self.cityCode
#import sys
#import imp
#imp.reload(sys)
#print (sys.getdefaultencoding())           
import csv
import random
import time
import socket
import http.client as httplib
import requests,html5lib
from bs4 import BeautifulSoup
import datetime
from datetime import time
#浏览器请求头，用于让网站识别是浏览器请求，避免反盗链将爬虫封杀
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3226.400 QQBrowser/9.6.11681.400'
}

class Spider():
      def urlText(self,url):
            self.timeout = random.choice(range(40,60))
            '''获取网页HTML代码，并解析成文本格式:
                  param url: 网页url地址:
                  return: 解析之后的html文本'''
            try:
                 respons = requests.get(url, headers=HEADERS,timeout=self.timeout)  # 获取网页信息
                 self.text = respons.content.decode('utf-8')  # 解析网页
                 #print (self.text)
                 return self.text
            except socket.timeout as e:
                  time.sleep(random.choice(range(8,15)))
            except socket.error as e:
                  time.sleep(random.choice(range(10,20)))
            except httplib.BadStatusLine as e:
                  time.sleep(random.choice(range(4,8)))
            except httplib.IncompleteRead as e:
                  time.sleep(random.choice(range(30,40)))
                        
      def get7d(self,url):
            '''获取需要的html标签：城市等。。。
                  :param url:
                  :param area: 区域：全国、全省(四川)  0:全国、其他任意值：全市
                  :return:'''
            text = self.urlText(url)
            soup = BeautifulSoup(text,'html5lib') #html5lib 容错性比lxml高
            div_tag = soup.find('div','c7d')
            ul = div_tag.find('ul','t clearfix') #find('ul',{'class':'t clearfix'})
            li  = ul.find_all('li')
            final7d = []
            ds = 0
            #now = datetime.datetime.now().strftime('%A %Y-%m-%d %H:%M:%S')
            for day in li:
                  temp = []
                  #date = day.find('h1').string.split('日')[0] #找到日期.split('(')[0]
                  delta = datetime.timedelta(days = ds)
                  date = datetime.datetime.now() + delta
                  temp.append(date.strftime('%A %Y-%m-%d').lower())
                  ds += 1
                  inf = day.find_all('p')
                  windf = inf[0].string
                  if '转' in windf:
                        windf = windf.split('转')[0]
                  temp.append(windf) #将第一个p中的内容天气情况加到temp中
                  if inf[1].find('span') is None:
                        tem_highest = None
                  else :
                        tem_highest = inf[1].find('span').string
                  tem_lowest = inf[1].find('i').string.replace('℃','')
                  temp.append([tem_highest,tem_lowest])
                  wind = inf[2].find('i').string
                  windx = inf[2].find('em').find_all('span')[0].attrs['title']
                  #print (windx)
                  if len(wind) > 4:
                        wind = wind[:4]
                  temp.append([windx,wind])
                  final7d.append(temp)    
            return final7d
            
if __name__=="__main__":
      code = getCityCode(r'city.json',r'上海').getCode()
      print(code)
      url = 'http://www.weather.com.cn/weather/{}.shtml'.format(code)
      w7d = Spider().get7d(url)
      print(w7d)
