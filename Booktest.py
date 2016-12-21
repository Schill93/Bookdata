try:
    import urllib.request as urllib2
    import os
    import sys
    import datetime
    import math
    import pymysql
    import urllib
    import lxml.html
    import requests
    import re
    from time import sleep
    from bs4 import BeautifulSoup as BS
except ImportError:
    import urllib2

outputFormat = 'db' # This is the standard mode in production
if len(sys.argv) > 1:
    if str(sys.argv[1]) == 'output=csv':
        outputFormat = 'csv' # This is a debug mode, writing output to local file only once

file = open('isbn.txt', 'r')

ISBNList = []  # Should be kept global so we don't get alot of calls, saves memory

for line in file:
    ISBNList.append(line)
file.close()

if outputFormat == 'db':
    passFile = open('passwd.txt', 'r')

    password = passFile.read()
    password = password.replace("\n","")


#Defines interval when the fetch should occur.
start = datetime.time(11, 00, 00)
end = datetime.time(12, 00, 00)




def bokus(isbn):

    link='http://www.bokus.com/bok/'


    try:
        response = urllib2.urlopen(link + isbn)

        html = response.read()
        # So we can handle it as string
        response.close()

    except:
        conn = False
        log("No connection to website. Trying to reconnect in 10 seconds.")
        sleep(10)

    try:
        soup = BS(html, 'lxml')

        buyValue = soup.find('span', {'class': 'pris big'}).text
        buyValue = buyValue[:-2]
    except:
        buyValue = 'null'
        buyValue = str(buyValue)

    return buyValue


def adlibris(isbn):


    link = 'http://www.adlibris.com/se/sok?q='


    try:
        response = urllib2.urlopen(link + isbn)

        html = response.read()
        # So we can handle it as string
        response.close()

    except:
        conn = False
        log("No connection to website. Trying to reconnect in 10 seconds.")
        sleep(10)

    try:

        soup = BS(html, 'lxml')

        buyValue = soup.find('div', {'class': 'current-price'}).text
        buyValue = buyValue[:-2]
    except:
        buyValue = 'null'
        buyValue = str(buyValue)

    return  buyValue

def snaplit(isbn):


    link = 'http://www.snaplit.com/?s='


    try:
        response = urllib2.urlopen(link + isbn)


        html = response.read()
        # So we can handle it as string
        response.close()

    except:
        conn = False
        sleep(10)


    try:
        soup = BS(html, 'lxml')

        buyValue = soup.find('span', {'class': "woocommerce-Price-amount amount"}).text
        buyValue = buyValue[:-2]
    except:
        buyValue='null'
        buyValue=str(buyValue)

    return buyValue



def cdon(isbn):

    link = 'http://cdon.se/search?q='


    try:
        response = urllib2.urlopen(link + isbn)


        html = response.read()
        # So we can handle it as string
        response.close()

    except:
        conn = False
        log("No connection to website. Trying to reconnect in 10 seconds.")
        sleep(10)

    try:

        soup = BS(html, 'lxml')

        error= soup.findAll('div', {'class': "support-message-wrapper"})

        buyValue = soup.findAll('div', {'class': "price"})



        price = str(int(re.search(r'\d+', str(buyValue[-1])).group()))
    except:
        price = 'null'
        price = str(price)

    if   error:
        price = 'null'
        price = str(price)


    return price

def db_create():

    conn = False

    while (conn == False):
        try:
            db = pymysql.connect(host='95.80.53.172', port=3306, user='stockmod', passwd=password, db='Bookprice')
            cursor = db.cursor()
            conn = True
        except:
            conn = False
            sleep(10)


    for isbn in ISBNList:

        try:
            sql = "CREATE TABLE `" + isbn.rstrip() + "` (date date, bokus double, adlibris double, cdon double, snaplit double, PRIMARY KEY (date));"
            cursor.execute(sql)
            db.commit()

        except:

                print(isbn.rstrip() + " already exists")
        else:
            print(isbn.rstrip() + " created")

    db.close()


def planner():
    conn = False

    while (conn == False):
        try:
            db = pymysql.connect(host='95.80.53.172', port=3306, user='stockmod', passwd=password, db='Bookprice')
            cursor = db.cursor()
            conn = True
        except:
            conn = False
            sleep(10)

    for isbn in ISBNList:
        sql = "INSERT INTO `" + isbn.rstrip() + "` (date, bokus, adlibris, cdon, snaplit) VALUES (CURDATE()," + bokus(
            isbn) + "," + adlibris(isbn) + "," + cdon(isbn) + "," + snaplit(isbn) + ");"
        print(sql)
        cursor.execute(sql)
        db.commit()

def fetch_to_file(output_file_name):

    rows = []
    rows.append("ISBN,bokus,adlibris,cdon,snaplit\n")

    for isbn in ISBNList:
        row = isbn.rstrip() + "," + bokus(isbn) + "," + adlibris(isbn) + "," + cdon(isbn) + "," + snaplit(isbn) + "\n"
        rows.append(row)
        print("Fetched ", row[:-1])

    print("Fetched data for " + str(len(rows)-1) + " books")

    with open(output_file_name, 'w') as out_file:
        out_file.writelines(rows)

    print("Wrote data to " + output_file_name)


def main():

    if outputFormat == 'db':
        db_create()

        while True:

            mydate = datetime.datetime.today()
            now = datetime.time(mydate.hour, mydate.minute, mydate.second)

            if start < now and now < end:
                planner()
                sleep(4000) #Sleep for over 1 h, so there is just i fetch per day.

            else:
                print('Going to sleep')
                sleep(600)
    elif outputFormat == 'csv':
        output_file_name = str((datetime.datetime.today()).isoformat()) + '.csv'
        output_file_path = "local_fetched_data/" # This directory has to exist beforehand
        fetch_to_file(output_file_path + output_file_name)



if __name__ == "__main__":
    main()

exit(0)