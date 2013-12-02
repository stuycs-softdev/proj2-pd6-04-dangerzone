#!/usr/bin/python
import json
from urllib import urlopen

# http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=Obama&FACET_FIELD=day_of_week&BEGIN_DATE=19000101
# &API-KEY=5772CD9A42F195C96DA0E930A7182688:14:68439177
# The original link is above. What happens is because we don't specify an end date, the panda article, which was
# coincidentally published today, becomes the first article that we see and gives us keywords like zoo.
# If we add an end date before then, then we can filter it out.

def ReturnRelatedTopics(Topic):
        NYT_API_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        API_KEY = "5772CD9A42F195C96DA0E930A7182688:14:68439177"
        FORMAT = "json"
        FQ = str(Topic)
        FACET_FIELD = "day_of_week"
        BEGIN_DATE = str(19000101)
        END_DATE = str(20131130)
        url = ("http://api.nytimes.com/svc/search/v2/articlesearch.%s?fq=%s&FACET_FIELD=%s&BEGIN_DATE=%s&END_DATE=%s&API-KEY=%s") % (FORMAT, FQ, FACET_FIELD, BEGIN_DATE, END_DATE, API_KEY)
        response = urlopen(url)
        Json_Data = json.loads(response.read())
        RELTOPICS = list()
        for y in Json_Data["response"]["docs"]:
            for x in y:
                if x == "keywords":
                    for a in y[x]:
                        RELTOPICS.append(a["value"])
        RELTOPICS.pop(0)
        RELTOPICS.pop(0)
        RELTOPICS.pop(0)

        return RELTOPICS

class Nytimes():
    def __init__(self, Topic):
        NYT_API_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        API_KEY = "5772CD9A42F195C96DA0E930A7182688:14:68439177"
        FORMAT = "json"
        FQ = str(Topic)
        FACET_FIELD = "day_of_week"
        BEGIN_DATE = str(19000101)
        END_DATE = str(20131130)
        url = ("http://api.nytimes.com/svc/search/v2/articlesearch.%s?fq=%s&FACET_FIELD=%s&BEGIN_DATE=%s&END_DATE=%s&API-KEY=%s") % (FORMAT, FQ, FACET_FIELD, BEGIN_DATE, END_DATE, API_KEY)
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
        print ReturnRelatedTopics("airplane")
