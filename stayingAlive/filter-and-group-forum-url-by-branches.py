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
	try : 
		nbPostsMin = int(float(sys.argv[3]))
	except :
		nbPostsMin = 15
except :
	print "\nError !! try : python prepare-url.py tree-yabiladi.csv yabiladi.com\n"
	sys.exit(0)

urlKeys = set()
urlTree = {}
topicsKeys = set()
topics = {}
authorsKeys = set()
authorsDict = {}

### open the urls file ###
with open(archivesFile) as f:
    archives = f.readlines()
# remove header
del archives[0]

### open the topics file ###
with open("topics-yabiladi.csv") as f:
    lines = f.readlines()
# remove header
del lines[0]

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
			first = float(urlTree[url]['first'].split('-')[2] + urlTree[url]['first'].split('-')[1] + urlTree[url]['first'].split('-')[0])
			curr = float(date.split('-')[2] + date.split('-')[1] + date.split('-')[0])
			if curr > last and updated == "True":
				urlTree[url]['last'] = date
			if curr < first:
				urlTree[url]['first'] = date				
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
			urlTree[url] = {'depth':len(uri[:-1]),'first':date,'last':date,'parent':parent,'hasChildren':hasChildren,'nbChildren':nbChildren,'descent':1,'cat':"",'topic':"",'nbPosts':"","authors":""}
			if not hasChildren and url in topicsKeys :
				urlTree[url]["cat"] = topics[url]["cat"]
				urlTree[url]["topic"] = topics[url]["topic"]
				urlTree[url]["nbPosts"] = topics[url]["nbPosts"]
				urlTree[url]["authors"] = topics[url]["authors"]
		
		addBranch(parent,uri[:-1],updated,date,True,wasNew)

def addKey(url,uri):
	if len(uri) == 0:
		return
	else:
		parent = "/".join(uri[:-1])
		urlKeys.add(url)
		addKey(parent,uri[:-1])

def prepareUrl(url):
	res = url.replace("https://","").replace("http://","").replace("www.","").replace(",","")
	res = res.replace(domName + ".",domName)
	res = res.replace(domName + ":80",domName)	
	return res	

def isForum(url):
	res = False
	tmp = url.split("/")
	if domName + "/forum" in url :
		res = True
	if url == "yabiladi.com" or url == "yabiladi.com/" :
		res = True
	if "/forum/profil" in url :
		res = False
	if "/forum/list" in url :
		res = False	
	if "/forum/login.php" in url :
		res = False	
	if "/forum/admin" in url :
		res = False	
	if "/forum/mods/" in url :
		res = False	
	if "folder_id=" in url :
		res = False	
	if "forum/register" in url :
		res = False	
	if "forum/addon" in url :
		res = False				
	if "/forum/control" in url :
		res = False
	if "/forum/read" in url :
		res = False	
	if "/forum/login" in url :
		res = False	
	if "/forum/edit" in url :
		res = False
	if "/forum/follow" in url :
		res = False						
	if "-quote=" in url :
		res = False	
	if ".html?" in url :
		res = False		

	return res 

def rewriteUrl(url):
	topic = re.findall("-[0-9]{1,2}-[0-9]*(?:.|-)", url)[0]
	first = url.split(topic)[0].split("/")
	title = first[len(first) - 1]
	last  = url.split(topic)[1]
	connector = topic[len(topic) -1]
	topic = topic[1:-1]
	tmp = "/".join(first[:-1]) + "/" + topic.split("-")[0] + "/" + topic.split("-")[1] + "/" + title + connector + last
	return tmp

### populate the dict of topics

nbTopics = len(lines)
cpt = 0

for line in lines :
	l = line.split(",")
	topicsKeys.add(l[1])

topics = dict.fromkeys(topicsKeys)

for k in topics :
	topics[k] = {}

for line in lines :
	print "Step 0 : " + str(cpt) + "/" + str(nbTopics)
	l = line.split(",")
	topics[l[1]]["cat"]   = l[2]
	topics[l[1]]["id"]    = l[0]
	topics[l[1]]["url"]   = l[1]
	topics[l[1]]["date"]  = l[3].split('T')[0].split('-')[2] + '-' + l[3].split('T')[0].split('-')[1] + '-' + l[3].split('T')[0].split('-')[0]
	topics[l[1]]["topic"] = l[4]
	topics[l[1]]["nbPosts"] = float(l[5])
	topics[l[1]]["authors"] = l[6][:-1]
	cpt +=1

nbUrls = len(archives)
cpt = 1

### populate the set of url key

for x in archives:
	print "Step 1 : " + str(cpt) + "/" + str(nbUrls)
	tmp = x.split(";")
	url = prepareUrl(tmp[1])
	if isForum(url) :
		if re.findall("-[0-9]{1,2}-[0-9]*(?:.|-)", url) is not None and len(re.findall("-[0-9]{1,2}-[0-9]*(?:.|-)", url)) > 0 :
			url = rewriteUrl(url)
			if url in topicsKeys and topics[url]["nbPosts"] >= nbPostsMin:
				addKey(url,url.split("/"))
		else :
			addKey(url,url.split("/")) 
	cpt = cpt + 1

urlTree = dict.fromkeys(urlKeys)
nbUrls  = len(urlTree)
cpt = 1

### populate the dict of url

for x in archives:
	print "Step 2 : " + str(cpt) + "/" + str(nbUrls) 
	tmp = x.split(";")
	url = prepareUrl(tmp[1])
	if isForum(url) :
		if re.findall("-[0-9]{1,2}-[0-9]*(?:.|-)", url) is not None and len(re.findall("-[0-9]{1,2}-[0-9]*(?:.|-)", url)) > 0 :
			url = rewriteUrl(url)
		if url in urlKeys :
			dateFirst = tmp[0]
			if url in topicsKeys :
				dateFirst = topics[url]["date"]
			addBranch(url,url.split("/"),tmp[2].strip(),dateFirst,False,False)
	cpt = cpt + 1

urlTree  = sorted(urlTree.items(), key=lambda (x, y): y['depth'])

nbBranch = len(urlTree)
keysArr  = []

# Populate the key array
cpt = 0
for branch in urlTree:
	print "Step 2 : " + str(cpt) + "/" + str(nbBranch - 1)
	authors = branch[1]["authors"].split(";")
	for a in authors :
		authorsKeys.add(a.split("|")[0])
	keysArr.append(getId(branch[0]))
	cpt = cpt + 1

authorsDict = dict.fromkeys(authorsKeys)
for a in authorsDict :
	authorsDict[a] = []

csv    = open("branches-forum-" + archivesFile.split("-")[1], "w") 
header = "url,first,last,id,parentId,hasChildren,nbChildren,descent,cat,topic,nbPosts,authors\n"
csv.write(header)

inf = None
sup = None
descent = 0
postSup = 0

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

	if branch[1]["nbPosts"] is not "" and branch[1]["nbPosts"] > postSup :
		postSup = branch[1]["nbPosts"] 

	authors = branch[1]["authors"].split(";")
	for a in authors :
		authorsDict[a.split("|")[0]].append({"topic":idBranch,"date":first})

	res = ""
	res += branch[0] + ","
	res += branch[1]["first"] + ","
	res += branch[1]["last"] + ","
	res += idBranch + ","
	res += idParent + ","
	res += str(branch[1]["hasChildren"]) + ","
	res += str(branch[1]["nbChildren"]) + ","
	res += str(branch[1]["descent"]) + ","
	res += branch[1]["cat"] + ","
	res += branch[1]["topic"] + ","
	res += str(branch[1]["nbPosts"]) + ","
	res += branch[1]["authors"] + "\n"
	csv.write(res)
	cpt = cpt + 1

csv    = open("authors-forum-" + archivesFile.split("-")[1], "w") 
header = "author,topics\n"
csv.write(header)

for a in authorsDict:
	tmp = sorted(authorsDict[a], key=lambda k: k['date'])
	topicList = ""
	for t in tmp :
		topicList += t["topic"] + "|"
	topicList = topicList[:-1]
	csv.write(a + "," + topicList + "\n")

meta = open("meta-forum-" + archivesFile.split("-")[1], "w")
meta.write(str(inf) + "\n")
meta.write(str(sup) + "\n")
meta.write(str(descent) + "\n")
meta.write(str(postSup) + "\n")