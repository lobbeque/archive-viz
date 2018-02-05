import sys
import requests
import json
import os
import re
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata
import operator

try :
	archivesFile = sys.argv[1]
except :
	print "\nError !! try : python prepare-url.py tree-atmf.csv\n"
	sys.exit(0)

urlTree = {}

with open(archivesFile) as f:
    archives = f.readlines()
# remove header
del archives[0]

def addBranch(url,uri,updated,date):

	if len(uri) == 0:
		return
	else:

		parent = "/".join(uri[:-1])
		
		if url in urlTree.keys():
			last = float(urlTree[url]['last'].split('-')[2] + urlTree[url]['last'].split('-')[1] + urlTree[url]['last'].split('-')[0])
			curr = float(date.split('-')[2] + date.split('-')[1] + date.split('-')[0])
			if curr > last and updated == "True":
				urlTree[url]['last'] = date
		else:
			urlTree[url] = {'depth':float(date.split('-')[2] + date.split('-')[1] + date.split('-')[0]),'first':date,'last':date,'parent':parent}
		
		addBranch(parent,uri[:-1],updated,date)



for x in archives:
	tmp = x.split(";")
	url = tmp[1].replace("http://","").replace("www.","").replace(",","")
	addBranch(url,url.split("/"),tmp[2].strip(),tmp[0])

urlTree = sorted(urlTree.items(), key=lambda (x, y): y['depth'])

csv    = open("branches-" + archivesFile.split("-")[1], "w") 
header = "url,first,last,parent\n"
csv.write(header)

for branch in urlTree:
	csv.write(branch[0] + "," + branch[1]["first"] + "," + branch[1]["last"] + "," + branch[1]["parent"] + "\n")

# print urlTree