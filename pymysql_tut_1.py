import bs4
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pymysql
#Go to webpage and scrape data

html = urlopen('https://en.wikipedia.org/wiki/List_of_largest_recorded_music_markets')
bsobj = soup(html.read(), "lxml")
tbody = bsobj('table',{'class':'wikitable plainrowheaders sortable'})[3].findAll('tr')
xl = []
for row in tbody:
    cols = row.findChildren(recursive = False)
    cols = tuple(element.text.strip().replace('%','') for element in cols)
    xl.append(cols)
xl = xl[1:-1]

print(xl)

# Open database connection
scrap_db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Lhy19931103', db='scraping')

# prepare a cursor object using cursor() method
cursor = scrap_db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS WIKI ")

# Create table as per requirement
sql = """CREATE TABLE WIKI (
 RANKING INT,
 MARKET CHAR(50),
 RETAIL_VALUE CHAR(20),
 PHYSICAL INT,
 DIGITAL INT,
 PERFORMANCE_RIGHTS INT,
 SYNCHRONIZATION INT
 )"""

cursor.execute(sql)


# Save data to the table

scrap_db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Lhy19931103', db='scraping')
mySql_insert_query = """INSERT INTO WIKI (RANKING, MARKET, RETAIL_VALUE, PHYSICAL,DIGITAL, PERFORMANCE_RIGHTS, SYNCHRONIZATION) 
VALUES (%s, %s, %s, %s ,%s, %s, %s) """

records_to_insert = xl

cursor = scrap_db.cursor()
cursor.executemany(mySql_insert_query, records_to_insert)
scrap_db.commit()
print(cursor.rowcount, "Record inserted successfully into WIKI2 table")

# disconnect from server
scrap_db.close()