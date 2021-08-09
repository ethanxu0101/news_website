import time
import requests
from src import db
from bs4 import BeautifulSoup





def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko)'}
    resp = requests.get(url, headers=headers)
    return resp.text


def get_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all('div', class_='cc-cd') # 注意别忘了class_参数后面的下划线
    return nodes


def get_sports():
    headers = {
        'user-agent ': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36',
    }

    url = 'https://tophub.today'
    html = get_html(url)
    nodes = get_nodes(html)

    now = int(time.time())
    for node in nodes:
        source = node.find('div', class_='cc-cd-lb').text.strip()
        if source not in ['微博', '知乎', 'IT之家', '哔哩哔哩', '虎扑社区', '机核网', 'CSDN论坛']:
            continue
        
        messages = node.find('div', class_='cc-cd-cb-l nano-content').find_all('a')
        for message in messages:
            content = message.find('span', class_='t').text.strip()

        data = {
                    'content': [content],
                    'url': [message['href']],
                    'source': [source],
                    'start_time': [now],
                    'end_time': [now]
                }

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




class News(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), primary_key=True)
    url = db.Column(db.String(60))
    source = db.Column(db.String(60))
    # year = db.Column(db.String(4))