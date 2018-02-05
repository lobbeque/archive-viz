import sys
import requests
import json
import os
import re
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata

# try :
# 	domain = sys.argv[1]
# 	batchSize = sys.argv[2]
# except :
# 	print "\nError !! try : python archive-to-url-tree.py yabiladi.com 100\n"
# 	sys.exit(0)

nb_list = 100

def getPages(url):
	# print url
	try :
		html = urlopen(url,data=None,timeout=10).read()
		return html
	except :
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

