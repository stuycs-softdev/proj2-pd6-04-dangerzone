#Aggregates all api calls and returns json object with the most relevant things



#This creates one box
class Aggregator():
    def __init__(self, topic):
        self.topic = topic
        self.hsw = howstuffworks()
        self.nytimes = nytimes()
        self.wiki = wikipedia()
        self.duckduckgo = duckduckgo()

    def createBox(topic):
        box = {}
        category = getCategory(self.topic)
        if(category == "person"):
            box = createPersonBox(self.topic)
        elif category == "place":
            box = createPlaceBox(self.topic)
        else:
            box = createDefaultBox(self.topic)
    def getCategory(topic):
        #For now just returns default... We can get back to this eventually
        if False:
            return "person"
        elif False:
            return "place"
        else:
            return "default"

    def createDefaultBox(topic):

        box = {}
        
        #Try to get links
        #Best option is nytimes
        #Let's see if we can get an image link    
        defi = getDefinition()
        if defi != "":
            box['Definition'] = defi

        box['HSWArticles'] = getHSWArticles()
        box['NyTimesArticles'] = getNYArticles()
        box['Videos'] = getYoutubeVideos()
        box['Images'] = getImages()
        box['Keyword'] = topic
        return box

    def createPersonBox(name):
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

    def getHSWArticles():
        articlesHSW = {}
        articlesHSW['Blurbs'] = []
        articlesHSW['Links'] = []
        i = 0
        for 0 in range(4):
            articles['Links'][i] = self.hsw.getArticle()
            articles['Blurbs'][i] = self.hsw.getBlurb()
            i += 1
    def getNYArticles():
        URL = 0
        HEADLINE = 1
        BLURB = 2
        i = 0
        articles = {}
        articles['Links'] = []
        articles['Blurbs'] = []
        articles['Headline'] = []
        for 0 in range(4):
            temp = self.nyt.getArticle()
            if not temp:
                return articles

            articles['Links'][i] = temp[URL]
            articles['Blurbs'][i] = temp[BLURB]
            articles['Headline'][i] = temp[HEADLINE]
            i += 1
        return articles

    def getYoutubeVideos():
        videos = {}
        i = 0
        videos['Title'] = []
        videos['Link'] = []
        for i in range(4):
            temp = self.utube.getVideo()
            videos['Title'][i] = temp[0]
            videos['Link'][i] = temp[1]
        return videos

    def getDefinition():
    definition = duck.getDefinition()
        if definition == "":
            definition = self.wiki.getDefinition()
    return definition

    def getImages():
        images = []
        i = 0
        for i in range(3):
            imgLink = self.goog.getImage()
            if imgLink != "":
                images[i] = imgLink
            else:
                break
            i += 1
        return images
