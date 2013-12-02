#!/usr/bin/python

import json
from urllib import urlopen

def ReturnRelatedTopics(Topic):
        NYT_API_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        API_KEY = "5772CD9A42F195C96DA0E930A7182688:14:68439177"
        FORMAT = "json"
        FQ = str(Topic)
        FACET_FIELD = "day_of_week"
        BEGIN_DATE = str(19000101)
        url = ("http://api.nytimes.com/svc/search/v2/articlesearch.%s?fq=%s&FACET_FIELD=%s&BEGIN_DATE=%s&API-KEY=%s") % (FORMAT, FQ, FACET_FIELD, BEGIN_DATE, API_KEY)
        response = urlopen(url)
        Json_Data = json.loads(response.read())
        RELTOPICS = list()
        for y in Json_Data["response"]["docs"]:
            for x in y:
                if x == "keywords":
                    for a in y[x]:
                        print a
                        RELTOPICS.append(a["value"])
        return RELTOPICS

class Nytimes():
    def __init__(self, Topic):
        NYT_API_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        API_KEY = "5772CD9A42F195C96DA0E930A7182688:14:68439177"
        FORMAT = "json"
        FQ = str(Topic)
        FACET_FIELD = "day_of_week"
        BEGIN_DATE = str(19000101)
        url = ("http://api.nytimes.com/svc/search/v2/articlesearch.%s?fq=%s&FACET_FIELD=%s&BEGIN_DATE=%s&API-KEY=%s") % (FORMAT, FQ, FACET_FIELD, BEGIN_DATE, API_KEY)
        response = urlopen(url)
        self.Json_Data = json.loads(response.read())

        URL = list()
        TITLE = list()
        SNIPPET = list()
        Counter = 0
        for x in self.Json_Data["response"]["docs"]:
            #print x
            URL.append(x["web_url"])
            TITLE.append(x["headline"]["main"])
            SNIPPET.append(x["snippet"])

        #print(URL)
        #print(TITLE)
        #print(SNIPPET)
        self.Data = zip(URL, TITLE, SNIPPET)
        self.counter = 0
        #print(Data)
        
    def getArticle(self):
        try:
            self.counter += 1
            return self.Data[self.counter - 1]
        except:
            return list()

    #End of class

    if __name__ == '__main__':
    #FindArticles("Obama")
        ReturnRelatedTopics("barrack obama")
