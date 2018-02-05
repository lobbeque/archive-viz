# Update extractor for a given site

import sys
import requests
import json
import os
import re
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata

# https://web.archive.org/web/2014*/www.ccme.org.ma
# https://web.archive.org/web/*/ccme.org.ma/*

# http://web.archive.org/cdx/search/cdx?url=yabiladi.com&from=2002&to=2002&matchType=prefix&filter=mimetype:text/html&filter=!url:.*archive.*&filter=statuscode:200&limit=100

url = "http://web.archive.org/cdx/search/cdx?matchType=prefix&filter=mimetype:text/html&filter=!url:.*archive.*"
dom = "yabiladi.com"

years  = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"] 
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
months_name = ["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"] 

try:
    os.remove("tree-" + name + ".csv")
except OSError:
    pass

csv    = open("tree-" + name + ".csv", "w") 
header = "date;url;updated\n"
csv.write(header)

def getSnapchot(url):
	try :
		html = urlopen(url,data=None,timeout=10).read()
	except :
		return

	soup  = BeautifulSoup.BeautifulSoup(html)
	lines = soup.getText().split("\n")
	tmp = ""
	for l in lines:
		f = l.split(" ")
		if len(f) < 7:
			continue
		date = f[1]
		y = date[0:4]
		m = date[4:6]
		d = date[6:8]
		date = d + "-" + m + "-" + y 
		print date
		digest = f[5]
		updated = tmp != digest
		tmp = digest
		url2 = f[2]
		row = date + ";" + url2 + ";" + str(updated) + "\n";
		csv.write(row)


# getSnapchot(url)

# def getArchives(dom,y,f,t):

# 	url += "&url=" + dom
# 	url += "&from=" + y
# 	url += "&to=" + y
# 	url += "&limit=" + limit

# 			 + 
# 			"&from=" + y + 
# 			"&to=" + y + 

# 			"&limit=5"
# 	try :
# 		html = urlopen(url,data=None,timeout=10).read()
# 		return html
# 	except :
# 		return None	




for year in years:
	html = getSnapchot