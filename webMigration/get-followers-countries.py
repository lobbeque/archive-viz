
import requests
import urllib
import urllib2
import json
from urllib2 import urlopen
import bs4 as BeautifulSoup
import sys
 
followers_country = {}

user = sys.argv[1]

if user is None:
	print "Add a user as argv please !"
	pass

# Open followers file

with open("list-followers-" + user + ".txt") as f:
    followers = f.readlines()
followers = [x.strip() for x in followers]  

# Write the results 

results  = open("list-countries-" + user + ".json", "w") 

def addCountry(name):
    print name
    if followers_country.get(name) is None:
        followers_country[name] = 1
    else :
        followers_country[name] = followers_country.get(name) + 1

# Get the location of the followers

count = 0

for follower in followers:

	done = False
	
	try:
	    page = urllib2.urlopen("https://twitter.com/" + follower)
	except urllib2.HTTPError, e:
	    print e.fp.read()

	html = page.read()  

	soup  = BeautifulSoup.BeautifulSoup(html)
	
	locations  = soup.findAll("span", { "class" : "ProfileHeaderCard-locationText" })

	if locations is not None and len(locations) > 0:
		
		location = locations[0].getText().strip()
		print location
		
		if location is not None and location is not "":

			# Call API

			r = requests.get("http://dev.virtualearth.net/REST/v1/Locations?query=" + location + "&key=AnBHiz8Vh1CJXio5aJ8EZY-fzJwMKfLCSIJnJ9YbC3U4NxDEjrUnm97beWE7guWv")

			if r.content is not None:
				data = json.loads(r.content)
				if len(data.get("resourceSets")) > 0 and data.get("resourceSets")[0].get("estimatedTotal") > 0:
					country = data.get("resourceSets")[0].get("resources")[0].get("address").get("countryRegion")
					if country is not None:
						print country
						done = True
						addCountry(country)

		count = count + 1
		print(count)
		if not done:
			addCountry("NONE")                            		

print followers_country
results.write(str(followers_country))