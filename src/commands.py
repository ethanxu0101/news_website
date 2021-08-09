# -*- coding: utf-8 -*-
import click
import time
import pandas as pd 

from src import app, db
from src.models import User, News

from src.utils import get_html, get_nodes, get_each_node_data, get_importance



@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
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

    for i, row in df.iterrows:
        n = News(title=row['title'], url=row['url'], source=row['source'], end_time=row['end_time'])
        db.session.add(n)

    db.session.commit()
    click.echo('Done.')



