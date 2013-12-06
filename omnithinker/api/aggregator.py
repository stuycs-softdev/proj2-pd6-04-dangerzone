#Aggregates all api calls and returns json object with the most relevant things

from logging import getLogger

from .howstuffworks import Howstuffworks
from .nytimes import Nytimes, ReturnRelatedTopics
from .youtube import Youtube
from .duckduckgo import Duckduckgo
from .google import Google

logger = getLogger("gunicorn.error")

# THIS IS A CLASS MOCK-UP UNTIL AARON CAN ADD IT BACK BECAUSE HE SEEMS TO HAVE
# FORGOTTEN ABOUT IT. HA, HA, GET IT? MOCK DUCK!?
#Function to be called...
def aggregate(startTopic):
    return makeBoxes(startTopic, 0, []) #Populates the boxes array

def makeBoxes(topic, depth, used):
    if depth >= 2 or topic in used:
        return
    else:
        used.append(topic)
        try:
            agg = Aggregator(topic)
            yield agg.createBox()
        except Exception as exc:
            logger.error("Error with topic " + topic + ": " + str(exc))
            return

    try:
        Related = ReturnRelatedTopics(topic)
    except Exception as exc:
        logger.error("Error with topic " + topic + ": " + str(exc))
    else:
        for newTopic in Related:
            for data in makeBoxes(newTopic, depth + 1, used):
                yield data

#This creates one box
class Aggregator():
    def __init__(self, topic):
        self.topic = topic
        self.hsw = Howstuffworks(topic)
        self.nyt = Nytimes(topic)
        #self.wiki = wikipedia()
        # self.youtube = Youtube(topic)
        self.duck = Duckduckgo(topic)
        try:
            self.goog = Google(topic)
        except:
            pass

    def getCategory(self):
        #For now just returns default... We can get back to this eventually
        if False:
            return "person"
        elif False:
            return "place"
        else:
            return "default"


    def createBox(self):
        box = {}
        category = self.getCategory()
        if(category == "person"):
            box = self.createPersonBox(self.topic)
        elif category == "place":
            box = self.createPlaceBox(self.topic)
        else:
            box = self.createDefaultBox(self.topic)
        return box

    def createDefaultBox(self, topic):
        box = {}

        box['Keyword'] = topic
        #Try to get links
        #Best option is nytimes
        #Let's see if we can get an image link
        defi = self.getDefinition()
        if defi != "":
            box['Definition'] = defi
        try:
            box['GoogleArticles'] = self.getGoogleArticles()
        except:
            pass
        box['HSWArticles'] = self.getHSWArticles()
        box['NyTimesArticles'] = self.getNYArticles()
        # box['Videos'] = self.getYoutubeVideos()
        try:
            box['Images'] = self.getImages()
        except:
            pass
        return box

    def createPersonBox(self, name):
        #We're going to use wiki here
        wiki = wikipedia()
        bday = wiki.getBday()
        dday = wiki.getDday() #Return Alive maybe?
        #Maybe profession?
        profession = wiki.getProfession()
        #Place of birth / categories
        imgLink = duck.getImage()


        box = {}
        box['Keyword'] = topic
        if bday != "":
            box['Bday'] = bday
        if dday != "":
            box['Dday'] = dday
        if profession != "":
            box['Profession'] = profession
        if imgLink != "":
            box['Image'] = imgLink

    def getHSWArticles(self):
        articles = {}
        articles['Blurbs'] = [0]*4
        articles['Links'] = [0]*4
        articles['Headline'] = [0]*4
        i = 0
        for i in range(4):
            articles['Links'][i] = self.hsw.getArticle()
            articles['Blurbs'][i] = self.hsw.getBlurb()
            articles['Headline'][i] = self.hsw.getHeadline()
        return articles
    def getNYArticles(self):
        URL = 0
        HEADLINE = 1
        BLURB = 2
        i = 0
        articles = {}
        articles['Links'] = [0]*4
        articles['Blurbs'] = [0]*4
        articles['Headline'] = [0]*4
        for i in range(4):
            temp = self.nyt.getArticle()
            if not temp:
                return articles

            articles['Links'][i] = temp[URL]
            articles['Blurbs'][i] = temp[BLURB]
            articles['Headline'][i] = temp[HEADLINE]
        return articles

    def getYoutubeVideos(self):
        videos = {}
        i = 0
        videos['Title'] = [0]*4
        videos['Link'] = [0]*4
        for i in range(4):
            temp = self.youtube.getVideo()
            if temp == "":
                return videos
            videos['Title'][i] = temp[0]
            videos['Link'][i] = temp[1]
        return videos

    def getDefinition(self):
        definition = self.duck.getDefinition()
        if definition == "":
#              definition = self.wiki.getDefinition()
            pass
        return definition
    def getGoogleArticles(self):
        URL = 1
        HEADLINE = 0
        BLURB = 2
        i = 0
        articles = {}
        articles['Links'] = [0]*4
        articles['Blurbs'] = [0]*4
        articles['Headline'] = [0]*4
        for i in range(4):
            temp = self.goog.getArticle()
            if not temp:
                return articles

            articles['Links'][i] = temp[URL]
            articles['Blurbs'][i] = temp[BLURB]
            articles['Headline'][i] = temp[HEADLINE]

        return articles

    def getImages(self):
        images = [0]*4
        i = 0
        for i in range(3):
            imgLink = self.goog.getImage()
            if imgLink != "":
                images[i] = imgLink
            else:
                break
            i += 1
        return images

if __name__ == "__main__":
    gen = aggregate("apples")
    for box in gen:
        print box
#      a = Aggregator("train")
#      box = a.createBox()
#      print "Printing def..."
#      print box['Definition']
#      print "Printing hsw articles"
#      print box['HSWArticles']
#      print "Printing nytimes articles"
#      print box['NyTimesArticles']
#      print "Printing videos..."
#      print box['Videos']
#      print json.loads(box)
