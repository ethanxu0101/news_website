# encoding: utf-8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import jieba
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
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


def get_each_node_data(df, nodes):
    # 获取当前时间
    now = int(time.time())

    # 遍历每个榜
    for node in nodes:
        # obtain the name in the nodes
        source = node.find('div', class_='cc-cd-lb').text.strip()
        # print(source)
        if source not in ['微博', 'IT之家', '哔哩哔哩', '虎扑社区', '机核网']:
            continue
        # obtain the content 
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

                item = pd.DataFrame(data)
                df = pd.concat([df, item], ignore_index=True)

            # 如果已经在数据库中，则更新相关信息
            else:
                index = df[df.content == content].index[0]
                df.at[index, 'end_time'] = now

    return df


def get_importance(row, corpus):
    importance = 0
    for each_word in corpus:
        if each_word in row['content']:
            importance += corpus[each_word]

    if row['source'] in ['微博']:
        importance = importance * 2

    return importance


url = 'https://tophub.today'
html = get_html(url)
nodes = get_nodes(html)

df = pd.DataFrame()
df = get_each_node_data(df, nodes)

# print(df.shape)
# print(df.head())
# df = pd.read_excel('test.xlsx')

## fliter news within one day
now = int(time.time())
df = df[df['end_time'] >= (now - 24 * 3600)]
df = df.dropna()

## generatr corpus database
content_list = df.content.to_numpy()
content_text = ''.join(content_list)
corpus_list = list(jieba.cut(content_text))

word_count = dict()
for each_word in corpus_list:
    if not each_word.isalpha():
        continue
    word_count[each_word] = word_count.get(each_word, 0) + 1

min_num = 1
max_num = 31
cleaned_corpus = dict()
for each_word in word_count:
    if min_num < word_count[each_word] < max_num:
        cleaned_corpus[each_word] = word_count[each_word]


# calculate the importance value for each news
df['importance'] = df.apply(lambda x: get_importance(x, cleaned_corpus), axis=1)

df = df.sort_values(by='importance', ascending=False).iloc[:40, ].copy()
print(df[['content', 'source', 'importance']].head(40))


engine = create_engine('sqlite:////home/user/Documents/news_website/test.db')  
df.to_sql('tophub', con=engine, if_exists='replace') 



app = Flask(__name__)

@app.route('/news')
def news_list():
    get_news()
    data = select_news()

    # print(len(data))
    return render_template('index4_short.html', data=data)
