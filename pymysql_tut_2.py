# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Handsome_Author   : Ethan
# @Time     : 2021/8/8 14:25

import requests
from lxml import etree

from pymysql import connect
# import mysql.connector

conn = connect(host='localhost', port=3306, database='scraping', user='root', password='Lhy19931103', charset='utf8')
# 获取cursor对象
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS SINA ")

# Create table as per requirement
sql = """CREATE TABLE SINA (
 TITLE CHAR(50),
 DATE CHAR(20),
 SOURCE CHAR(50),
 URL CHAR(100),
 CONTENT CHAR(50)
 )"""

cursor.execute(sql)



#存mysql函数
def save_sql(sqli,values):
    cursor.execute(sqli, values)
    conn.commit()

def get_sports():
    headers = {
        'user-agent ': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36',
    }

    url = 'https://sports.sina.com.cn/'

    try:
        res = requests.get(url=url,headers=headers)
    except:
        res = requests.get(url=url, headers=headers)

    res_text = etree.HTML(res.text)

    url_list = res_text.xpath("//div[@class='ty-top-ent']//a[contains(@href,'shtml')]/@href")

    # url_list = list(dict.fromkeys(url_list))
    url_list = list(set(url_list))
    print('Total Number of URL List: ',len(url_list))

    # print(url_list[2:10])
    for x in url_list[2:10]:
        print(x)
        if 'zt_d' not in x:
            try:
                res2 = requests.get(url=x, headers=headers)
            except:
                res2 = requests.get(url=x, headers=headers)
            # print(res2.encoding)
            try:
                data = res2.text
                data = data.encode('ISO-8859-1')
                data = data.decode('utf-8')
            except:
                continue
            res2_text = etree.HTML(data)

            """
            item has keys: title, date, time, source, url, content
            
            """

            item = {}
            item['title'] = ''.join(res2_text.xpath("//h1[@class='main-title']/text()"))
            date = res2_text.xpath("//span[@class='date']/text()")

            try:
                item['date'] = ''.join(date[0].split(" ")[0])
                item['time'] = ''.join(date[0].split(" ")[1])
                item['source'] = ''.join(res2_text.xpath("//div[@class='date-source']//a/text()"))
                item['url'] = x
            except:
                continue
            # item['content'] = ''.join(res2_text.xpath("//div[@class='article']/p/text()")).replace('\r','').replace('\n','').replace('\t','').replace('\u3000','').replace('  ','').replace('\xa0 ','')

            print(item)

            sqli = '''INSERT INTO SINA(TITLE, DATE, SOURCE, URL)
                                                values(%s,%s,%s,%s)
                                                '''
            values = (item['title'], item['date'], item['source'], item['url'])


            # save_sql(sqli, values)
            try:
                save_sql(sqli, values)
                print('Store in database successfully')
            except:
                conn.rollback()  # 如果发生错误则回滚
                print('Somehow failure')

    print('Finish Sports News Scraping')

if __name__ == '__main__':
    get_sports()
