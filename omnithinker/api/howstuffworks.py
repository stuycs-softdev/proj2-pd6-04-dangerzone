import urllib2

from bs4 import BeautifulSoup

class Howstuffworks():
    def __init__(self, topic):
        link="http://www.howstuffworks.com/search.php?terms="
        words = topic.split(' ')
        for word in words:
            link += (word + '+')
        link = link.rstrip('+')
        page = urllib2.urlopen(link)
        data = page.read()
        self.soup = BeautifulSoup(data)
        self.blurbIter = 0

    def getArticle(self): #Uses blurbs iterable function
        i = 0
        for link in self.soup.find_all('div'):
            try:
                if link['class'][0] == "c1":
                    if self.blurbIter == i:
                        return link.a['href']
                    i += 1
            except:
                pass
    def getBlurb(self): #Iterable function...
        i = 0
        for link in self.soup.find_all('div'):
            try:
                if link['class'][0] == "c2":
                    if self.blurbIter == i:
                        self.blurbIter += 1;
                        return link.p.get_text()
                    i += 1
            except:
                pass
        return ""

if __name__ == "__main__":
    h = Howstuffworks("Obama")
    print h.getArticle()
