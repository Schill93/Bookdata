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


response = urllib2.urlopen('http://www.bokus.com/bok/9789144067650/analys-i-en-variabel/')

html=response.read()

response.close()

soup = BS(html, "lxml")

title = soup.find("meta",  itemprop="price")



print(title['content'])