from urllib2 import urlopen
import json

class Google():
    def __init__(self):
        GoogleSearch("Apples")

    def GoogleSearchArticles(topic):
        DEVELOPER_KEY = "AIzaSyCmBiXQBlUnuYehSvCcM_5CxNuT2hu41Qs"
        response = urlopen('https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s' % (DEVELOPER_KEY, topic))
        Json_Data = json.loads(response.read())
        print('https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s' % (DEVELOPER_KEY, topic))
        print(Json_Data)

        TITLE = list()
        URL = list()
        SNIPPET = list()

        for x in Json_Data["items"]:
            TITLE.append(x["title"])
            URL.append(x["link"])
            SNIPPET.append(x["snippet"])

        print("Printing TITLE")
        print(TITLE)
        print("Printing URL")
        print(URL)
        print("Printing SNIPPET")
        print(SNIPPET)
        data = zip(TITLE, URL, SNIPPET)
        return data

    def GoogleSearchImages(topic):
        DEVELOPER_KEY = "AIzaSyCmBiXQBlUnuYehSvCcM_5CxNuT2hu41Qs"
        response = urlopen('https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s&searchType=image' % (DEVELOPER_KEY, topic))
        Json_Data = json.loads(response.read())
        print('https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s&searchType=image' % (DEVELOPER_KEY, topic))
        print(Json_Data)

        IMAGES = list()
        for x in Json_Data["items"]:
            IMAGES.append(x["image"]["contextLink"])

        return IMAGES





