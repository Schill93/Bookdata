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


response = urllib2.urlopen('https://www.akademibokhandeln.se/sok/?sokfraga=9789144067650')

html=response.read()

response.close()

soup = BS(html, "lxml")

title = soup.find('span', 'list-product-price__large list-product-price__large--2').text  #.text gör att den bara returnerar värdet, och inte hela"strängen"


print(title)