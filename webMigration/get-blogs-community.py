
import requests
import urllib
import urllib2
import json
from urllib2 import urlopen
import bs4 as BeautifulSoup
import sys
import dryscrape
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

community  = open("list-community-larbi.txt", "w") 
results = []

# with open("list-posts-sonofwords.txt") as f:
#     posts = f.readlines()

# capabilities = webdriver.DesiredCapabilities().FIREFOX
# capabilities["marionette"] = False
# binary = FirefoxBinary(r'/usr/bin/firefox')
# driver = webdriver.Firefox(firefox_binary=binary, capabilities=capabilities)

# for post in posts:

# 	print post

# 	driver.wait = WebDriverWait(driver, 5)
# 	driver.get(post)
# 	try:
# 		driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "comment-header")))
# 		html = driver.page_source
		
# 		soup  = BeautifulSoup.BeautifulSoup(html)

# 		users  = soup.findAll("cite", { "class" : "user" })

# 		for user in users:
# 			print user.getText().strip()
# 			results.append(user.getText().strip())
# 	except TimeoutException:
# 		print("No comment")

try:
	page = urllib2.urlopen("http://www.larbi.org/archive")
except urllib2.HTTPError, e:
	print e.fp.read()

html     = page.read() 	
soup     = BeautifulSoup.BeautifulSoup(html)
archives = soup.findAll("a")

for archive in archives:
	if "archive/" in archive['href']:
		
		try:
			page = urllib2.urlopen(archive['href'])
		except urllib2.HTTPError, e:
			print e.fp.read()

		print archive['href']

		html  = page.read() 	
		soup  = BeautifulSoup.BeautifulSoup(html)
		posts = soup.findAll("a")

		for post in posts:
			if "post/" in post['href']:

				try:
					page = urllib2.urlopen(post['href'])
				except urllib2.HTTPError, e:
					print e.fp.read()

				html  = page.read() 	
				soup  = BeautifulSoup.BeautifulSoup(html)
				comments = soup.findAll("dt", {"class":"odd"})

				for comment in comments:
					results.append(comment.getText().split('par ')[1].strip())			

uniqUsers = set(results)

for user in uniqUsers:
	community.write(user.encode('utf8') + "\n")

