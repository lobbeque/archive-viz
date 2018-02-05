import sys
import requests
import json
import os
import re
import bs4 as BeautifulSoup
import unicodedata
import csv 

from urllib2 import urlopen

tree  = []
root  = True
header = True

source = "tree-blogreda.csv"
target = "tree-blogreda.json"

def findParent(cpt,url,tree):
    if cpt <= 0 :
        return tree[0]["url"]
    elif tree[cpt]["url"] in url:
        return tree[cpt]["url"]
    else :
    	return findParent(cpt - 1,url,tree)

branch_cpt = 0
with open(source, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
    	if header :
    		header = False
    		continue

        if root :
            root = False
            node  = {"url":"","parent":"/","date":[],"updated":[]}
            node["url"] = row[1]
            node["date"].append(row[0])
            node["updated"].append(row[2])
            tree.append(node)
        elif row[1] == tree[branch_cpt]["url"] :
            tree[branch_cpt]["date"].append(row[0])
            tree[branch_cpt]["updated"].append(row[2])
        else :
            node  = {"url":"","parent":findParent(branch_cpt,row[1],tree),"date":[],"updated":[]}
            node["url"] = row[1]
            node["date"].append(row[0])
            node["updated"].append(row[2]) 
            tree.append(node)
    	    branch_cpt = branch_cpt + 1

with open(target, 'w') as outfile:
    json.dump(tree, outfile)





