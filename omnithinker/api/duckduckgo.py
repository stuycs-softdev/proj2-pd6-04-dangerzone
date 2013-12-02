import urllib2 
import json

#look up a topic DuckDuckGo
#Handle disambiguity
#Specfics, if person (look for word biography), then give info on them
class Duckduckgo:
    def __init__(self, topic):
        link = "http://api.duckduckgo.com/?q=" + topic + "&format=json"
        data = urllib2.urlopen(link)
        self.info = json.loads(data.read()) 

    def getDefinition(self):
        try:
            definition = self.info['Definition']
            return definition
        except:
            return ""
    def getBlurb(self):
        try:
            text = (self.info['RelatedTopics'][0]['Text'])
        except:
            text = ""
        try:
            text1 = (self.info['RelatedTopics'][1]['Text'])
        except:
            text1 = ""
        try:
            text2 = (self.info['RelatedTopics'][2]['Text'])
        except:
            text2 = "" 

        num1 = len(text.split(' '))
        num2 = len(text1.split(' '))
        num3 = len(text2.split(' '))
        if num1 > 7:
            return text
        elif num2 > 7:
            return text1
        elif num3 > 7:
            return text2

        return ""
    def getImageLink(self):
        try:
            print self.amerca
            return self.info['RelatedTopics'][0]['Icon']['URL']
        except:
            try:
                return self.info['RelatedTopics'][2]['Icon']['URL']
            except:
                return ""

        return ""

