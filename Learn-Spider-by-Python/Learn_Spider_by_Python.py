#%%
#使用BeautifulSoup获取博客标题
import requests
from bs4 import BeautifulSoup

link = 'http://www.santostang.com/'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
r = requests.get(link,headers=headers)

soup = BeautifulSoup(r.text,"html.parser")
first_title = soup.find('h1',class_='post-title').a.text.strip()
print('第一篇文章的标题是：',first_title)

title_list = soup.find_all('h1',class_='post-title')
for i in range(len(title_list)):
    title = title_list[i].a.text.strip()
    print('第%s篇文章的标题是：%s' % (i + 1,title))

#%%
#使用正则表达式re包抓取博客主页所有文章标题
import requests
import re

link = "http://www.santostang.com/"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
r = requests.get(link,headers=headers)
html = r.text

#()表明要匹配的、解析出来的表达式
title_list = re.findall('<h1 class="post-title"><a href=.*?>(.*?)</a></h1>',html)
print(title_list)


#%%
#正则表达式 re包
#re.match方法，从字符串起始位置匹配一个模式，如果从起始位置匹配不了，返回none
#即匹配的字符必须首字符相同
import re
m = re.match('www','www.santostang.com')
print('匹配的结果：',m)
print('匹配的起始和终点：',m.span())
print('匹配的起始位置：',m.start())
print('匹配的终点位置：',m.end())

line = "Fat cats are smarter than dogs, is it right?"
m = re.match(r'(.*) are (.*?) dogs', line)
print('匹配的整句话',m.group(0))
print('匹配的第一个结果',m.group(1))
print('匹配的第二个结果',m.group(2))
print('匹配的结果列表',m.groups())

#re.search方法，扫描整个字符串，返回第一个成功的匹配
m_match = re.match('com','www.santostang.com')
m_search = re.search('com','www.santostang.com')
print(m_match)
print(m_search)

#re.findall方法，找到所有匹配
#'[0-9]+'表示任意长度的数字
m_match = re.match('[0-9]+','12345 is the first number, 23456 is the second')
m_search = re.search('[0-9]+','12345 is the first number, 23456 is the second')
m_findall = re.findall('[0-9]+','12345 is the first number, 23456 is the second')
print(m_match.group())
print(m_search.group())
print(m_findall)

#%%
#%% test 朝阳信息股票评分抓取
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import csv

driver = webdriver.Chrome()
driver.get("https://advcaifuhao.antfortune.com/p/q/jeo2a9tl/pages/home/index.html?stock_code=600986")

name = driver.find_element_by_css_selector('p.name')
score = driver.find_element_by_css_selector('p.score')
print(name.text)
print(score.text)

output_list = {name.text,score.text}
with open('test.csv','a+',newline='') as csvfile:
    w = csv.writer(csvfile)
    w = writerow(output_list)

#%%
#拔取安居客数据
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
link = 'https://beijing.anjuke.com/sale/'
r = requests.get(link, headers = headers)

soup = BeautifulSoup(r.text, 'lxml')
house_list = soup.find_all('li', class_="list-item")

for house in house_list:
    name = house.find('div', class_ ='house-title').a.text.strip()
    price = house.find('span', class_='price-det').text.strip()
    price_area = house.find('span', class_='unit-price').text.strip()

    no_room = house.find('div', class_='details-item').span.text
    area = house.find('div', class_='details-item').contents[3].text
    floor = house.find('div', class_='details-item').contents[5].text
    year = house.find('div', class_='details-item').contents[7].text
    broker = house.find('span', class_='brokername').text
    broker = broker[1:]
    address = house.find('span', class_='comm-address').text.strip()
    address = address.replace('\\xa0\\xa0\\n                    ','  ')
    tag_list = house.find_all('span', class_='item-tags')
    tags = [i.text for i in tag_list]
    print(name, price, price_area, no_room, area, floor, year, broker, address, tags)

#%%
#Selenium模拟浏览器抓取
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://www.santostang.com/2017/03/02/hello-world/")

#%%
#动态网页抓取
#AJAX,找到真实数据地址,获取json格式数据
#提取jason数据中的评论
import requests
import json

link = "https://api-zero.livere.com/v1/comments/list?callback=jQuery112406696618820172218_1526302134189&limit=1000&repSeq=3871836&requestPath=%2Fv1%2Fcomments%2Flist&consumerSeq=1020&livereSeq=28583&smartloginSeq=5154&_=1526302134191"
headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
r = requests.get(link,headers=headers)
print(r.text)

json_string = r.text
json_string = json_string[json_string.find('{'):-2]

json_data = json.loads(json_string)
comment_list = json_data['results']['parents']

for eachone in comment_list:
    message = eachone['content']
    print(message)

#%%
#Requests爬虫实践：豆瓣电影TOP250电影数据
#豆瓣已经使用Cookies封禁，因此该方法已不能成功
import requests
from bs4 import BeautifulSoup

def get_movies():
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
        'Host':'https://movie.douban.com/'
    }
    movie_list = []
    for i in range(0,10):
        link = 'https://movie.douban.com/top250?start=' + str(i * 25) + 'filter='
        r = requests.get(link,headers=headers,timeout=100)
        print(str(i + 1),'页响应状态码：',r.status_code)

        soup = BeautifulSoup(r.text,"lxml")
        div_list = soup.find_all('div',class_= 'hd')
        for each in div_list:
            movie = each.a.span.text.strip()
            movie_list.append(movie)
    return movie_list

movies = get_movies()
print(movies)

#%%
#超时
import requests
link = 'http://www.santostang.com/'
r = requests.get(link,timeout = 0.1)

#%%
#定制请求头，浏览器，检查，Network，单击需要请求的网页，在Headers中可以看到Request Headers
import requests
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
    'Host':'www.santostang.com'
    }
r = requests.get('http://www.santostang.com',headers=headers)
print('响应状态码：',r.status_code)


#%%
#传递URL参数
import requests
key_dict = {'key1':'value1','key2':'value2'}
r = requests.get('http://httpbin.org/get',params=key_dict)
print('URL已经正确编码：',r.url)
print('字符串方式的响应体：\n',r.text)

#%%
#获取响应内容
#200请求成功
#4XX客户端错误
#5XX服务器错误响应
import requests
r = requests.get('http://www.santostang.com/')
print('文本编码：',r.encoding)
print('响应状态码：',r.status_code)
print('字符串方式的响应体：',r.text)

#%%
import operator
x = {1:2,3:4,4:3,2:1,0:0}
sorted_x = sorted(x.items(),key=operator.itemgetter(1))
print(sorted_x)

#%%
#爬虫简单应用，提取标题
import requests
from bs4 import BeautifulSoup

link = "http://www.santostang.com/"
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1;en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
r = requests.get(link,headers=headers)

soup = BeautifulSoup(r.text,'lxml')
title = soup.find("h1",class_="post-title").a.text.strip()
print(title)

#%%
#类的封装与继承
#注意
class Animal:
    def eat(self):
        print("%s 吃" % self.name)
    def drink(self):
        print("%s 喝" % self.name)
    def shit(self):
        print("%s 拉" % self.name)
    def pee(self):
        print("%s 撒" % self.name)
class Cat(Animal):
    def __init__(self,name):
        self.name = name
    def cry(self):
        print('喵喵叫')
class Dog(Animal):
    def __init__(self,name):
        self.name = name
    def cry(self):
        print('汪汪叫')

c1 = Cat('小白家的小黑猫')
c1.eat()
c1.cry()

d1 = Dog('胖子家的小瘦狗')
d1.eat()

#%%
#遍历字典4种方法：
namebook = {'Name':'Alex','Age':7,'Class':'First'}

#该方法必须保证字典集的值是整型
#for key in namebook:
#    print(key + ':' + namebook[key])

#for key in namebook.keys:
#    print(key + ':' + namebook[key])
for kv in namebook.items():
    print(kv)

for key,value in namebook.items():
    print(key,'+',value) 
