#Aggregates all api calls and returns json object with the most relevant things

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
    box['Title'] = topic

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
    link2 = duckduckgo.getLink()
    #Let's see if we can get an image link
    hswlinks = {}
    hswlinks['Blurbs']   
    hswlinks['Links']   
    for 0 in range(4):
        hswlinks['Links'][i] = hsw.getArticle()
        hswlinks['Blurbs'][i] = hsw.getBlurb()
    box['Links'] = []
    box['Links'][0] = hswlinks
    link1 = nyt.getArticle() #Returns tuple headline, link
    if link1 != "":
        box['Links'][1] = link1()
    imgLink = duckduckgo.getImage()
    if imgLink != "":
        box['Image'] = imgLink
def createPersonBox(name):
    #We're going to use wiki here
    wiki = wikipedia()
    bday = wiki.getBday()
    dday = wiki.getDday()
    #Maybe profession?
    #Place of birth / categories

