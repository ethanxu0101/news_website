import requests
from bs4 import BeautifulSoup
import time
import pandas
import re
from sqlalchemy import create_engine


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko)'}
    resp = requests.get(url, headers=headers)
    return resp.text

def get_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all('div', class_='cc-cd') # 注意别忘了class_参数后面的下划线
    return nodes


url = 'https://tophub.today'
html = get_html(url)
nodes = get_nodes(html)

def get_each_node_data(df, nodes):
    # 获取当前时间
    now = int(time.time())

    # 遍历每个榜
    for node in nodes:
        # 获得榜单的名字
        source = node.find('div', class_='cc-cd-lb').text.strip()
        # print(source)
        if source not in ['微博', '知乎', 'IT之家', '哔哩哔哩', '虎扑社区', '机核网', 'CSDN论坛']:
            continue
        # 获取榜单里的数据内容
        messages = node.find('div', class_='cc-cd-cb-l nano-content').find_all('a')
        for message in messages:
            content = message.find('span', class_='t').text.strip()

            # 如果不在数据库中，就添加新的数据
            if df.empty or df[df.content == content].empty:
                # 注意创建新的DataFrame的时候，即使只有一条数据，也需要用列表
                data = {
                    'content': [content],
                    'url': [message['href']],
                    'source': [source],
                    'start_time': [now],
                    'end_time': [now]
                }

                item = pandas.DataFrame(data)
                df = pandas.concat([df, item], ignore_index=True)

            # 如果已经在数据库中，则更新相关信息
            else:
                index = df[df.content == content].index[0]
                df.at[index, 'end_time'] = now

    return df


url = 'https://tophub.today'
html = get_html(url)
nodes = get_nodes(html)

df = pandas.DataFrame()
df = get_each_node_data(df, nodes)


# path = r'C:\Users\yixu\Documents\Git_Project\news_website'
engine = create_engine('sqlite:///test.db')  # path为数据库的路径(推荐写成绝对路径)
df.to_sql('tophub', con=engine, if_exists='replace') # table为保存数据库table的名字，可以随便写，DataFrame会为为什么自动创建

print(df.shape)
print(df.head())

