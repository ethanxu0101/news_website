"""
Target: news scraping and show the content simultaneously 
combination of: flask_tut_3 and pymysql_tut_2
"""


from numpy import empty
import pymysql
import pandas as pd
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from openpyxl import Workbook  


def get_news():

    # connect to the database
    conn = pymysql.connect(host="localhost", user="root", passwd="Lhy19931103", db="scraping", port=3306, charset="utf8")

    cursor = conn.cursor()
    sql='select * from sina'
    cursor.execute(sql)
    row = cursor.fetchone()  # fetch one row data

    num = 0
    all = []

    while row is not None:

        row = cursor.fetchone()
        num += 1

        all.append(row)
        if num > 350:
            break
        else:
            pass

    cursor.close()
    conn.close()

    all = tuple(all)
    wb = Workbook() # generate a workbook
    sheet = wb.active # activate the workbook sheet
    sheet.title = 'Entertainment'  # name the current sheet
    sheet.append(['Title','Date','Source', 'URL']) # generate the desired the columns 
    for j in all:
        try:
            sheet.append(tuple(j))  
        except:
            pass
    wb.save('./today_news_entertainment.xlsx') # save out


def select_news():
    df = pd.read_excel('./today_news_entertainment.xlsx')

    df = pd.DataFrame(df, columns=['Title','URL'])

    the_sum = []

    for x in range(1,5):
        z = df.iloc[x, :].values
        # print(5555,z)
        if z is not empty:
            the_sum.append(z)
        else:
            continue
    return the_sum


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:root:Lhy19931103@127.0.0.1:3306/scraping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class News(db.Model):
    title = db.Column(db.String(50), primary_key=True)
    date = db.Column(db.String(20))
    source = db.Column(db.String(20))
    url = db.Column(db.String(100))

@app.route('/')
def index():
    # 删除所有继承db.Model的表
    db.drop_all()

    # 创建所有继承db.Model的表
    db.create_all()

    # 创建对象（模型）
    news_object = News(name='zs')

    # 将对象添加到会话（事物）中
    db.session.add(news_object)

    # 提交会话（事物），必须提交，否则数据库不会变化
    db.session.commit()
    return 'index'

@app.route('/news')
def news_list():
    get_news()
    data = select_news()
    return render_template('index4_short.html', data=data)


if __name__ == '__main__':
    app.run()