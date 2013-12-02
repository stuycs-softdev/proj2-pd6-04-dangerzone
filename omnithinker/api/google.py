from urllib2 import urlopen
import json

class Google():
    def __init__(self, topic):
        self.articles = self.GoogleSearchArticles(topic)
        self.images = self.GoogleSearchImages(topic)
        self.icounter = 0
        self.acounter = 0
    def GoogleSearchArticles(self, topic):
        DEVELOPER_KEY = "AIzaSyCSO5JoLloaoPsO4QJ_NS1PEh4TepSTtgI"
        string = ""
        words = topic.split(' ')
        for word in words:
            string += word + '+'
        string = string.rstrip('+')
        print 'https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s' % (DEVELOPER_KEY, string)
        response = urlopen('https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s' % (DEVELOPER_KEY, string))
        Json_Data = json.loads(response.read())

        TITLE = list()
        URL = list()
        SNIPPET = list()

        for x in Json_Data["items"]:
            TITLE.append(x["title"])
            URL.append(x["link"])
            SNIPPET.append(x["snippet"])

        data = zip(TITLE, URL, SNIPPET)
        return data

    def GoogleSearchImages(self, topic):
        DEVELOPER_KEY = "AIzaSyCSO5JoLloaoPsO4QJ_NS1PEh4TepSTtgI"
        string = ""
        words = topic.split(' ')
        for word in words:
            string += word + '+'
        string = string.rstrip('+')
        response = urlopen('https://www.googleapis.com/customsearch/v1?key=%s&cx=015867020359405023218:wnembc1eg9m&q=%s&searchType=image' % (DEVELOPER_KEY, string))
        Json_Data = json.loads(response.read())

        IMAGES = list()
        for x in Json_Data["items"]:
            IMAGES.append(x["image"]["contextLink"])

        return IMAGES

    def getImage(self):
        if not self.images[self.icounter]:
            return ""
        else:
            self.icounter += 1
            return self.images[self.icounter - 1]

    def getArticle(self):
        if not self.articles[self.acounter]:
            return ""
        else:
            self.acounter += 1
            return self.articles[self.acounter - 1]
if __name__ == "__main__":
    g = Google("Train")
    print g.getArticle()
    print g.getImage()

    print g.getArticle()

    print g.getImage()
