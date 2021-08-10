import time
import requests
import pandas as pd
from src import db
from bs4 import BeautifulSoup
from src.utils import get_html, get_nodes, get_each_node_data, get_importance, filter_news



def forge():
    """Generate fake data."""

    print('start generating')
    db.create_all()

    name = 'Ethan Xu'
    user = User(name=name)
    db.session.add(user)

    url = 'https://tophub.today'
    html = get_html(url)
    nodes = get_nodes(html)

    df = pd.DataFrame()
    df = get_each_node_data(df, nodes)

    now = int(time.time())
    df = df[df['end_time'] >= (now - 24 * 3600)]
    df = df.dropna()

    df = filter_news(df)


    for i, row in df.iterrows():
        n = News(id = i, title=row['title'], url=row['url'], source=row['source'], end_time=row['end_time'])
        db.session.add(n)

    db.session.commit()


def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    url = db.Column(db.String(60))
    source = db.Column(db.String(60))
    end_time = db.Column(db.String(4))