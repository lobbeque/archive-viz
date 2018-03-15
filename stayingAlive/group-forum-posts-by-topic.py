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

catCpt = 100

results = {}

def rewriteUrl(url):
	url = url.replace("https://","").replace("http://","").replace("www.","").replace(",","")
	topic = re.findall("-[0-9]{1,2}-[0-9]*(?:.|-)", url)[0]
	first = url.split(topic)[0].split("/")
	title = first[len(first) - 1]
	last  = url.split(topic)[1]
	connector = topic[len(topic) -1]
	topic = topic[1:-1]
	tmp = "/".join(first[:-1]) + "/" + topic.split("-")[0] + "/" + topic.split("-")[1] + "/" + title + connector + last
	return tmp

def getId(s):
	return	hashlib.sha256(s).hexdigest()	

csv    = open("topics-yabiladi.csv", "w") 
header = "id,url,cat,date,topic,nbPosts,authors\n"
csv.write(header)


while catCpt > 0:

	postKey = set()
	postArr = []

	try :
		# open posts file
		with open("yabiladi-forum-" + str(catCpt) + ".csv") as f:
			lines = f.readlines()
		# remove header
		del lines[0]

		for l in lines:
			post = l.split(',')
			post[6] = rewriteUrl(post[6])
			post[5] = getId(post[6])
			post[2] = post[2].replace("|"," ").replace(";"," ")
			postKey.add(post[6])
			postArr.append(post)

		topics = dict.fromkeys(postKey)

		for k in topics:
			topics[k] = {}
			topics[k]["authors"] = {}
			topics[k]["id"] = ""

		for p in postArr:
			k = p[6]
			if topics[k]["id"] == "" :
				# first time
				topics[k]["cat"]   = catCpt
				topics[k]["id"]    = p[5]
				topics[k]["url"]   = k
				topics[k]["date"]  = p[4]
				topics[k]["topic"] = p[8]
				topics[k]["nbPosts"] = 1
				topics[k]["authors"][p[2]] = 1 
			else :
				# add a post 
				topics[k]["nbPosts"] += 1
				if p[4] < topics[k]["date"] :
					topics[k]["date"] = p[4]
				if p[2] in topics[k]["authors"] :
					topics[k]["authors"][p[2]] += 1
				else :
					topics[k]["authors"][p[2]] = 1	

		for k in topics:
			res =  topics[k]["id"] + ","
			res += topics[k]["url"] + ","
			res += str(topics[k]["cat"]) + ","
			res += topics[k]["date"] + ","
			res += topics[k]["topic"] + ","
			res += str(topics[k]["nbPosts"]) + ","
			tmp = "" 
			for a in topics[k]["authors"] :
				if a.strip() != "" :
					tmp += a + "|" + str(topics[k]["authors"][a]) + ";"
			tmp = tmp[1:-1]
			res += tmp + "\n"
			csv.write(res)

	except IOError:
		print "missing file " + "yabiladi-forum-" + str(catCpt) + ".csv"

	catCpt -=1

