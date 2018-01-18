import requests
import urllib
import urllib2
import json
from urllib2 import urlopen
import bs4 as BeautifulSoup
import sys
import re

community  = open("list-stable-community-larbi.txt", "w") 
stable = []

with open("list-community-larbi.txt") as f:
    userBlog = f.readlines()
userBlog = [x.lower() for x in userBlog]  

with open("list-followers-larbi_org.txt") as f:
    userTwitter = f.readlines()    
userTwitter = [x.lower() for x in userTwitter]

print "Blog : " + str(len(userBlog))

for user in userBlog:
	for foll in userTwitter:
		if user in foll or foll in user: 
			stable.append(user)

uniqUsers = set(stable)

print "Stable : " + str(len(uniqUsers))

print uniqUsers

for s in uniqUsers:
	community.write(s + "\n")