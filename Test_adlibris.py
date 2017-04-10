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


response = urllib2.urlopen('http://www.adlibris.com/se/sok?q=9789144067650')

html=response.read()

response.close()

soup = BS(html, "lxml")

title = soup.find('div', {'class': 'current-price'}).text  #.text gör att den bara returnerar värdet, och inte hela"strängen"


print(title)