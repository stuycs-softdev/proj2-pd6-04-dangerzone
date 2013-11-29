#!/usr/bin/python

import json
from urllib import urlopen

NYT_API_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'

def FindArticles(Topic):
    API_KEY = "5772CD9A42F195C96DA0E930A7182688:14:68439177"
    FORMAT = "json"
    FQ = str(Topic)
    FACET_FIELD = "day_of_week"
    BEGIN_DATE = str(19000101)

    url = ("http://api.nytimes.com/svc/search/v2/articlesearch.%s?fq=%s&FACET_FIELD=%s&BEGIN_DATE=%s&API-KEY=%s") % (FORMAT, FQ, FACET_FIELD, BEGIN_DATE, API_KEY)
    response = urlopen(url)
    Json_Data = json.loads(response.read())
    print url
    print Json_Data

    URL = list()
    TITLE = list()
    Snippet = list()
    Counter = 0
    # for x in Json_Data["response"]["Docs"]:
    #     if x == "web_url":
    #         Counter = Counter + 1
    #         URL.append(Json_Data["response"]["Docs"][x])
    #         print("Hello!")


    return Json_Data

if __name__ == '__main__':
    FindArticles("Obama")
