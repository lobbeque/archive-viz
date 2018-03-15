import sys
import requests
import json
import os
import re
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
import unicodedata
import hashlib

reload(sys)
sys.setdefaultencoding('utf8')

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

months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
months_name = ["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"]        

nb_list = 97

def getPages(url):
	req = urllib2.Request(url, headers=hdr)

	try:
		html = urllib2.urlopen(req).read()
		return html
	except urllib2.HTTPError, e:
		print e.fp.read()
		return None

def getNbPages(url):
	html = getPages(url)
	soup = BeautifulSoup.BeautifulSoup(html)
	pagination = soup.findAll("a", {"class":"curr"})
	if len(pagination) > 0 :
		nb_pages = int(float(pagination[-1].getText().strip()))
	else :
		nb_pages = 1	
	return nb_pages

def isValid(d):
	date = d.split(' ')

	if len(date) > 3 :
		month = getUnicode(date[1].strip())
		try :
			return months_name.index(month) >= 0
		except :
			return False
	else :
		return False

def formatDate(d):
	date = d.split(' ')
	month = getUnicode(date[1].strip())
	post_date = date[2] + "-" + months[months_name.index(month) - 1] + '-' + date[0].zfill(2) + 'T' + date[3] + ":00" 
	return post_date

def getId(s):
	return	hashlib.sha256(s).hexdigest()

def getUnicode(s):
	return unicodedata.normalize('NFD', s).encode('ascii', 'ignore')

while nb_list > 0 :
	list_url = "https://www.yabiladi.com/forum/list/" + str(nb_list) + "/"
	html = getPages(list_url)
	if html is not None :
		soup = BeautifulSoup.BeautifulSoup(html)
		list_name = soup.find(id="refrechListF")
		if list_name is not None :
			topic_category = getUnicode(list_name.getText().replace(","," "))
			print "###"
			print topic_category
			print "###"
			csv    = open("yabiladi-forum-" + str(nb_list) + ".csv", "w") 
			header = "post_id,post_idx,post_author,post_author_id,post_date,topic_id,topic_url,topic_category,topic_title,topic_date,topic_author,topic_author_id\n"
			csv.write(header)			
			pagination = soup.findAll("a", {"class":"curr"})
			if len(pagination) > 0 :
				nb_pages = int(float(pagination[-1].getText().strip()))
			else :
				nb_pages = 1
			
			i = 1
			while i <= nb_pages :
				list_url_tmp = list_url + "page=" + str(i)
				html = getPages(list_url_tmp)
				if html is not None :
					soup = BeautifulSoup.BeautifulSoup(html)
					for a in soup.findAll("a",{"class":"title"}) :
						topic_url = "http:" + a['href']
						print topic_url
						nb_posts = getNbPages(topic_url)
						# print nb_posts
						j = 1
						post_cpt = 1
						while j <= nb_posts :
							html = getPages(topic_url.replace(".html","-page=" + str(j) + ".html"))
							if html is not None :
								# print "inside !"
								soup = BeautifulSoup.BeautifulSoup(html)
								posts = soup.findAll("div",{"class":"com-header"})
								if j == 1  :
									# print "first"
									# First post of the topic 
									topic_id = getId(topic_url.replace(".html","-page=" + str(j) + ".html"))
									topic_title = soup.find("div",{"class":"title_forum_new"}).getText().strip().replace(","," ")
									print topic_title									
									topic_author = posts[0].find("a").getText().strip().replace(","," ")
									topic_author_id = getId(getUnicode(topic_author))
									topic_date_tmp = posts[0].find("div",{"class":"com-date"}).getText().strip().replace(","," ")
								if isValid(topic_date_tmp) :
									# print "date is valide !"
									topic_date = formatDate(topic_date_tmp)
									for post in posts :
										date_tmp = post.find("div",{"class":"com-date"}).getText().strip().replace(","," ")
										if isValid(date_tmp) :
											post_date = formatDate(date_tmp)
											post_idx = post_cpt
											post_author = post.find("a").getText().strip().replace(","," ")
											post_author_id = getId(getUnicode(post_author))
											post_id = topic_id + str(post_idx)
											results = post_id + ',' + str(post_idx) + ',' + post_author + ',' + post_author_id + ','
											results = results + post_date + ',' + topic_id + ',' + topic_url + ',' + topic_category + ','
											results = results + topic_title + ',' + topic_date + ',' + topic_author + ',' + topic_author_id + '\n'
											post_cpt += 1
											csv.write(results)
							j += 1 
				i += 1
	nb_list -= 1

