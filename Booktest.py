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



file = open('isbn.txt', 'r')

ISBNList = []  # Should be kept global so we don't get alot of calls, saves memory

for line in file:
    ISBNList.append(line)
file.close()

print(ISBNList)


def bokus():

    print('bokus')

    link='http://www.bokus.com/bok/'

    for x in range (0,2):
        try:
            response = urllib2.urlopen(link + ISBNList[x])

            html = response.read()
            # So we can handle it as string
            response.close()

        except:
            conn = False
            log("No connection to website. Trying to reconnect in 10 seconds.")
            sleep(10)

        soup = BS(html, 'lxml')

        buyValue = soup.find('span', {'class': 'pris big'}).text
        buyValue = buyValue[:-2]
        print(buyValue)

        sleep(1)

def adlibris():
    print('adlibris')

    link = 'http://www.adlibris.com/se/sok?q='

    for x in range(0, 2):
        try:
            response = urllib2.urlopen(link + ISBNList[x])

            html = response.read()
            # So we can handle it as string
            response.close()

        except:
            conn = False
            log("No connection to website. Trying to reconnect in 10 seconds.")
            sleep(10)

        soup = BS(html, 'lxml')

        buyValue = soup.find('div', {'class': 'current-price'}).text
        buyValue = buyValue[:-2]
        print(buyValue)

def snaplit():
    print('snaplit')

    link = 'http://www.snaplit.com/?s='

    for x in range(0, 2):
        try:
            response = urllib2.urlopen(link + ISBNList[x])


            html = response.read()
            # So we can handle it as string
            response.close()

        except:
            conn = False
            log("No connection to website. Trying to reconnect in 10 seconds.")
            sleep(10)

        soup = BS(html, 'lxml')

        buyValue = soup.find('span', {'class': "woocommerce-Price-amount amount"}).text
        buyValue = buyValue[:-2]
        print(buyValue)


def main():
    bokus()
    adlibris()
    #cdon()
    snaplit()



if __name__ == "__main__":
    main()
