import sys
import requests
import json
import os
import re
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata

domain = ""
batchSize = ""

try :
	domain = sys.argv[1]
	batchSize = sys.argv[2]
except :
	print "\nError !! try : python archive-to-url-tree.py yabiladi.com 100\n"
	sys.exit(0)

years = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"]

url = "http://web.archive.org/cdx/search/cdx?url=" + domain + "&matchType=prefix&filter=mimetype:text/html&filter=!url:.*archive.*&showResumeKey=true&limit=" + batchSize

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

lastDigest = ""

csv    = open("tree-" + domain.split('.')[0] + ".csv", "w") 
header = "date;url;updated\n"
csv.write(header)

def getPages(url):
	req = urllib2.Request(url, headers=hdr)
	try:
		html = urllib2.urlopen(req).read()
		return html
	except urllib2.HTTPError, e:
		print e.fp.read()
		return None


for year in years :
	print year + " processing ..."
	next = True
	currentUrl = url + "&from=" + year + "&to=" + year
	print currentUrl
	resumeKey = None
	while next :
		if resumeKey is None :
			html = getPages(currentUrl)
			print html
		else :
			html = getPages(currentUrl + "&resumeKey=" + resumeKey)

		if html is None or html == "" :
			next = False
		else :
			print "coucou"
			soup  = BeautifulSoup.BeautifulSoup(html)
			lines = soup.getText().split("\n")

			print lines[len(lines)-2]
			if "text\/html" in lines[len(lines)-2] :
				next = False
			else :
				resumeKey = lines[len(lines) - 2]
				lines = lines[:-3]

			for l in lines:
				f = l.split(" ")
				if len(f) < 7:
					continue
				date = f[1]
				y = date[0:4]
				m = date[4:6]
				d = date[6:8]
				date = d + "-" + m + "-" + y 
				digest = f[5]
				updated = lastDigest != digest
				lastDigest = digest
				url2 = f[2]
				print date + ";" + url2 + ";" + str(updated)
				row = date + ";" + url2 + ";" + str(updated) + "\n";
				csv.write(row)	
