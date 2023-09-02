import requests
from threading import Thread
import math
import json
import os

LEETCODE_API_LINK = "https://leetcode.com/contest/api/ranking/"
PAGE_COUNT = 1
TOTAL_REGISTRATIONS = 0
FILE_NAME = ""
db = {}

#generate the api link from the contest name and api endpoint
def getContestLink():
    name = input("Enter LeetCode Contest Name (example: biweekly-contest-112)")
    if len(name) == 0:
        name = "biweekly-contest-112"
    global FILE_NAME
    FILE_NAME = name + ".txt"
    link = LEETCODE_API_LINK + name + '/'
    return link

#get data from one page of leetcode rankings
def getPageData(pageNumber,url):
    global db
    response = requests.get(url,{'pagination':pageNumber,'region':'global'})
    print("Page : "+str(pageNumber) + " Loaded")
    rjson = response.json()
    f = open(FILE_NAME,"a")
    for ranker in rjson['total_rank']:
        db[ranker['rank']] = {"rank":ranker['rank'],"username":ranker['username']}
        f.write(json.dumps(db[ranker['rank']]))
        f.write("\r\n")
    f.close()

#load from local file
def loadDBFromFile():
    global db
    f = open(FILE_NAME,'r')
    for line in f:
        line = line[:-1]
        js = json.loads(line)
        db[js['rank']] = js

#getting rank data from leetcode or local file and saving it to a local file
def populateDatabase(contestLink):
    print(contestLink)
    if(os.path.exists(FILE_NAME)):
        loadDBFromFile()
        return
    currentPage = 1
    response = requests.get(contestLink,{'pagination':1,'region':'global'})
    rjson = response.json()
    MAX_USERS_PER_PAGE = 25
    MAX_PAGE_COUNT = math.ceil(rjson['user_num']/MAX_USERS_PER_PAGE)
    for currentPage in range(1,MAX_PAGE_COUNT+1):
        t = Thread(target = getPageData , args=[currentPage,contestLink])
        t.run()

#Printing Rank Wise Data
def printData(db):
    for rank in db:
        t = str(rank)
        while len(t)<6:
            t= t+ ' '
        print('Rank : '+ t + ' -> Username : '+db[rank]['username'])

contestLink = getContestLink()
populateDatabase(contestLink)
printData(db)