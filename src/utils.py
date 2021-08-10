import time
import pandas as pd
import jieba
import requests
from bs4 import BeautifulSoup


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
    item_list = []
    for node in nodes:
        # obtain the name in the nodes
        source = node.find('div', class_='cc-cd-lb').text.strip()
        # print(source)
        if source not in ['微博', 'IT之家', '哔哩哔哩', '虎扑社区', '机核网']:
            continue
        # obtain the content 
        messages = node.find('div', class_='cc-cd-cb-l nano-content').find_all('a')

        for message in messages:
            title = message.find('span', class_='t').text.strip()

            data = {
                'title': [title],
                'url': [message['href']],
                'source': [source],
                'start_time': [now],
                'end_time': [now]
            }

            item = pd.DataFrame(data)
            item_list.append(item)

    df = pd.concat(item_list, ignore_index=True)

    return df


def get_importance(row, corpus):
    importance = 0
    for each_word in corpus:
        if each_word in row['title']:
            importance += corpus[each_word]

    if row['source'] in ['微博']:
        importance = importance * 2

    return importance


def filter_news(df, num_news):
    ## generatr corpus database
    title_list = df.title.to_numpy()
    title_text = ''.join(title_list)
    corpus_list = list(jieba.cut(title_text))

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
    
    df['importance'] = df.apply(lambda x: get_importance(x, cleaned_corpus), axis=1)

    assert num_news > 0, "Please give a positive number"

    num_news = min(num_news, df.shape[0])
    df = df.sort_values(by='importance', ascending=False).iloc[:num_news, ].copy()

    return df