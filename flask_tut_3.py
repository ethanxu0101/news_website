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

@app.route('/news')
def news_list():
    get_news()
    data = select_news()
    return render_template('index4_short.html', data=data)


if __name__ == '__main__':
    app.run()