import sys
import requests
import json
import os
import re
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata

# try :
# 	domain = sys.argv[1]
# 	batchSize = sys.argv[2]
# except :
# 	print "\nError !! try : python archive-to-url-tree.py yabiladi.com 100\n"
# 	sys.exit(0)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

nb_list = 100

def getPages(url):
	print url
	req = urllib2.Request(url, headers=hdr)

	try:
		page = urllib2.urlopen(req)
		return html.read()
	except urllib2.HTTPError, e:
		print e.fp.read()
		return None

while nb_list > 0 :
	list_url = "https://www.yabiladi.com/forum/list/" + str(nb_list) + "/"
	html = getPages(list_url)
	print html
	if html is not None :
		soup = BeautifulSoup.BeautifulSoup(html)
		list_name = soup.find(id="refrechListF").getText()
		print list_name

	print nb_list
	nb_list -= 1

