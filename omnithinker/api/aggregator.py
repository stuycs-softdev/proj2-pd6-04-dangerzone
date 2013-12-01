#Aggregates all api calls and returns json object with the most relevant things
URL = 0
HEADLINE = 1
BLURB = 2

#This creates one box
def createBox(topic):
    box = {}
    category = getCategory(topic)
    if(category == "person"):
        box = createPersonBox(topic)
    elif category == "place":
        box = createPlaceBox(topic)
    else
        box = createDefaultBox(topic)
def getCategory(topic):
    if False:
        return "person"
    elif False:
        return "place"
    else:
        return "default"

def createDefaultBox(topic):

    #try to get definition
    box = {}

    #Init the different api objects
    duck = duckduckgo()
    wiki = wikipedia()
    nyt = nytimes()
    hsw = howstuffworks()
    #Try to get definition
    definition = duck.getDefinition()
    if definition == "":
        definition = wiki.getDefinition()
    if definition != "":
        box['definition'] = definition 

    #Try to get links
    #Best option is nytimes
    linkNY = nyt.getArticle() #Returns tuple headline, link
    linkDDG = duckduckgo.getLink()
    #Let's see if we can get an image link
    articles = {}
    articles['Blurbs'] = []
    articles['Links'] = []
    i = 0
    for 0 in range(4):
        articles['Links'][i] = hsw.getArticle()
        articles['Blurbs'][i] = hsw.getBlurb()
        i += 1
    for 0 in range(4):
        temp = nyt.getArticle()
        articles['Links'][i] = temp[URL]
        articles['Blurbs'][i] = temp[BLURB]
        articles['Headline'][i] = temp[HEADLINE]
        i += 1
    
    images = []
    j = 0
    for i in range(3):
        imgLink = goog.getImage()
        if imgLink != "":
            box['Image'][i] = imgLink
        else:
            break
        j += 1
    
    videos = []
    k = 0
    for i in range(4):

    box = {}
    box['Keyword'] = topic
    box['Articles'] = articles
    box['Images'] = images
    box['Videos'] = videos
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

