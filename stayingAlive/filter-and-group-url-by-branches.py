import sys
import requests
import json
import os
import re
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata
import operator
import hashlib

try :
	archivesFile = sys.argv[1]
	domName = sys.argv[2]
except :
	print "\nError !! try : python prepare-url.py tree-atmf.csv atmf.org\n"
	sys.exit(0)

keysSet = set()
urlTree = {}

with open(archivesFile) as f:
    archives = f.readlines()
# remove header
del archives[0]

def getId(s):
	return	hashlib.sha256(s).hexdigest()

def addBranch(url,uri,updated,date,hasChildren,wasNew):

	if len(uri) == 0:
		return
	else:

		parent = "/".join(uri[:-1])
		depth = len(uri[:-1])
		
		if urlTree[url] is not None :
			last = float(urlTree[url]['last'].split('-')[2] + urlTree[url]['last'].split('-')[1] + urlTree[url]['last'].split('-')[0])
			curr = float(date.split('-')[2] + date.split('-')[1] + date.split('-')[0])
			if curr > last and updated == "True":
				urlTree[url]['last'] = date
			urlTree[url]['hasChildren'] = hasChildren
			if hasChildren and wasNew :
				urlTree[url]['nbChildren'] = urlTree[url]['nbChildren'] + 1
			if hasChildren :
				urlTree[url]['descent'] = urlTree[url]['descent'] + 1
			wasNew = False
		else:
			if hasChildren :
				nbChildren = 1
			else :
				nbChildren = 0
			wasNew = True
			urlTree[url] = {'depth':len(uri[:-1]),'first':date,'last':date,'parent':parent,'hasChildren':hasChildren,'nbChildren':nbChildren,'descent':1}
		
		addBranch(parent,uri[:-1],updated,date,True,wasNew)

def addKey(url,uri):
	if len(uri) == 0:
		return
	else:
		parent = "/".join(uri[:-1])
		keysSet.add(url)
		addKey(parent,uri[:-1])

def prepareUrl(url):
	res = url.replace("https://","").replace("http://","").replace("www.","").replace(",","")
	res = res.replace(domName + ".",domName)
	res = res.replace(domName + ":80",domName)	
	return res		

nbUrls = len(archives)
cpt = 1

# Populate the set of keys
for x in archives:
	tmp = x.split(";")
	url = prepareUrl(tmp[1])
	addKey(url,url.split("/"))
	print "Step 0 : " + str(cpt) + "/" + str(nbUrls) 
	cpt = cpt + 1

urlTree = dict.fromkeys(keysSet)
cpt = 1

# Populate the dict
for x in archives:
	print "Step 1 : " + str(cpt) + "/" + str(nbUrls) 
	tmp = x.split(";")
	url = prepareUrl(tmp[1])
	# url = re.sub('/$', '', url)
	addBranch(url,url.split("/"),tmp[2].strip(),tmp[0],False,False)
	cpt = cpt + 1

urlTree  = sorted(urlTree.items(), key=lambda (x, y): y['depth'])
nbBranch = len(urlTree)
keysArr  = []

csv    = open("keys-" + archivesFile.split("-")[1], "w") 
header = "url,idFull,idSmall\n"
csv.write(header)

cpt = 0
for branch in urlTree:
	print "Step 2 : " + str(cpt) + "/" + str(nbBranch - 1)
	keysArr.append(getId(branch[0]))
	csv.write(branch[0] + "," + getId(branch[0]) + "," + str(cpt) + "\n")
	cpt = cpt + 1

csv    = open("branches-" + archivesFile.split("-")[1], "w") 
header = "url,first,last,id,parentId,hasChildren,nbChildren,descent\n"
csv.write(header)

inf = None
sup = None
descent = 0

cpt = 1
for branch in urlTree:
	print "Step 3 : " + str(cpt) + "/" + str(nbBranch)
	first = float(branch[1]["first"].split('-')[2] + branch[1]["first"].split('-')[1] + branch[1]["first"].split('-')[0])
	last  = float(branch[1]["last"].split('-')[2] + branch[1]["last"].split('-')[1] + branch[1]["last"].split('-')[0])
	idBranch = str(keysArr.index(getId(branch[0])))
	try :
		idParent = str(keysArr.index(getId(branch[1]["parent"])))
	except :
		idParent = ""
	if inf is None or first < inf :
		inf = first
	if sup is None or first > sup :
		sup = first 
	if (branch[1]["depth"] > 0 and float(branch[1]["descent"]) > descent) :
		descent = float(branch[1]["descent"])
	csv.write(branch[0] + "," + branch[1]["first"] + "," + branch[1]["last"] + "," + idBranch + "," + idParent + "," + str(branch[1]["hasChildren"]) + "," + str(branch[1]["nbChildren"]) + "," + str(branch[1]["descent"]) + "\n")
	cpt = cpt + 1

meta = open("meta-" + archivesFile.split("-")[1], "w")
meta.write(str(inf) + "\n")
meta.write(str(sup) + "\n")
meta.write(str(descent) + "\n")