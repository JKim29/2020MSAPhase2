import ast
import requests
import urllib.request
import bs4 as bs
import pandas as pd
import datetime
import os
from datetime import timedelta

path = "C:/Users/Jordan/Desktop/MSA/2020/Phase 2/"

# Method of finding current day
def addDays(num):
    return ((num / 6) * 7)

base_d = datetime.datetime(2020, 9, 10) # 15996
base_d - timedelta(days = 7) # 15990

initial_d = base_d - timedelta(days = addDays(15996)) # 0 - Inital day

initial_d + timedelta(days = addDays(16002))

response = requests.get('https://forum.netmarble.com/api/game/nanagb/official/forum/7ds_en/article/list?rows=15&start=0&menuSeq=1&_=1600263540539')
r = response.json()

newList = []

# Extracting date and reaction information
for page in r["articleList"]:
    newDict = {}
    newDict["regDate"] = int(str(page["regDate"])[:5])
    newDict["reactionInfo"] = page["reactionInfo"]
    newList.append(newDict)

dateList = []
posList = []
neuList = []
negList = []
# 1-Love, 2-Haha, 3-Like, 4-Wow, 5-Sad, 6-Angry
# 1,2,3 - Positive, 4 - Neutral, 5,6 - Negative

# Creating a total count of each category of sentiment
for ele in newList:
    negCount = 0
    neuCount = 0
    posCount = 0
    count = 1
    for reaction in ele["reactionInfo"]:
        reactionCount = reaction["cnt"]
        if count <= 3:
            posCount += reactionCount
        elif count == 4:
            neuCount += reactionCount
        else:
            negCount += reactionCount
        count += 1

    if ele["regDate"] in dateList:
        index = dateList.index(ele["regDate"])
        posList[index] += posCount
        neuList[index] += neuCount
        negList[index] += negCount
    else:
        dateList.append(ele["regDate"])
        posList.append(posCount)
        neuList.append(neuCount)
        negList.append(negCount)

# Creating a percentage positive list
sentimentList = []
for i in range(len(dateList)):
    sentimentList.append(posList[i]/(posList[i] + neuList[i] + negList[i]))
    dateList[i] = initial_d + timedelta(days = addDays(dateList[i]))
    dateList[i] = dateList[i].strftime("%Y-%m-%d")

# New DataFrame
webScrape = pd.DataFrame({
    "Days":dateList,
    "PercentPos":sentimentList
})

# Saving as csv
dataDir = os.getcwd() + "\\data\\"
dataScrape = dataDir + "webScrape.csv"

webScrape.to_csv(dataScrape, index=False)