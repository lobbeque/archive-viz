# https://apps.twitter.com/app/14629949

# gmaps AIzaSyBDF3bz_A1kvi07Wh2mkXXZoZTA1G3nKmM 

import tweepy
from tweepy import OAuthHandler
import requests
import urllib
import urllib2
import json
import operator
from urllib2 import urlopen
import bs4 as BeautifulSoup
 
# App authorisation

# consumer_key = 'U8A64n5hKs919yk9Cwd0iYX51'
# consumer_secret = 'aFaysBONMeP9Q5wx50OpBYfSM5JS8Sk8B1rAae4GJPQtIpD10W'
# access_token = '917359578349752320-g5QVPwzg5sYbHCIEgblvLNIjc6swlOk'
# access_secret = 'JVTlAM3tP6BNZXCCYSOFdLZAVm5OQvTeF5KhKrCD8mEJY'
 
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)
 
# api = tweepy.API(auth)

# GeoLoc
followers_country = {}

# Write
user = "oef75"

try:
    page = urllib2.urlopen("https://twitter.com/JossSheldon")
except urllib2.HTTPError, e:
    print e.fp.read()

html = page.read()  

soup  = BeautifulSoup.BeautifulSoup(html)
location  = soup.findAll("span", { "class" : "ProfileHeaderCard-locationText" })

print location

# results  = open("followers-" + user + ".json", "w") 

# def addCountry(name):
#     print name
#     if followers_country.get(name) is None:
#         followers_country[name] = 1
#     else :
#         followers_country[name] = followers_country.get(name) + 1


# count = 0
# try:
#     for fl in tweepy.Cursor(api.followers, screen_name=user, wait_on_rate_limit=True).items():
#         # Process the friend here
#         # print "###"
#         print fl.location

#         done = False

#         if fl.location is not None and fl.location is not "":
            
#             # r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + fl.location + "&key=AIzaSyBDF3bz_A1kvi07Wh2mkXXZoZTA1G3nKmM")

#             r = requests.get("http://dev.virtualearth.net/REST/v1/Locations?query=" + fl.location + "&key=AnBHiz8Vh1CJXio5aJ8EZY-fzJwMKfLCSIJnJ9YbC3U4NxDEjrUnm97beWE7guWv")

#             if r.content is not None:
#                 data = json.loads(r.content)
#                 if len(data.get("resourceSets")) > 0 and data.get("resourceSets")[0].get("estimatedTotal") > 0:
#                     country = data.get("resourceSets")[0].get("resources")[0].get("address").get("countryRegion")
#                     if country is not None:
#                             done = True
#                             addCountry(country)
#         count = count + 1
#         print(count)
#         if not done:
#             print fl.location
#             addCountry("NONE")
# except tweepy.error.TweepError:
#     print followers_country    

# print followers_country
# results.write(str(followers_country))
# sorted_followers = sorted(followers_country.items(), key=operator.itemgetter(1), reverse=True)
# print sorted_followers
