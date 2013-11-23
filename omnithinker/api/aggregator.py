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
    #Try to get definition
    definition = duck.getDefinition()
    if definition == "":
        definition = wiki.getDefinition()
    if definition != "":
        box['definition'] = definition
    
    #Try to get links
    #Best option is nytimes
    link1 = nyt.getArticle() #Returns tuple headline, link
    if not link:
        link =

