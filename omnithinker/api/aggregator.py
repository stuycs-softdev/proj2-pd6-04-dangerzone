from logging import getLogger

from .duckduckgo import Duckduckgo
from .google import Google
from .howstuffworks import Howstuffworks
from .nytimes import Nytimes
from .wikipedia import Wikipedia
from .youtube import Youtube

logger = getLogger("gunicorn.error")

def aggregate(topic):
    """Aggregate all data sources.

    Generates a series of JSON objects with the most relevant information for
    the given start topic, then for topics related to the start topic, then for
    topics related to those, etc.
    """
    def make_boxes(topic, depth, used):
        if depth > (1 if len(used) > 10 else 2) or topic.lower() in used:
            return
        used.append(topic.lower())
        agg = Aggregator(topic)
        yield agg.create_box()
        for new_topic in agg.wiki.get_related_topics():
            for box in make_boxes(new_topic, depth + 1, used):
                yield box
    return make_boxes(topic, 0, [])


class Aggregator(object):
    """Creates one box."""
    def __init__(self, topic):
        self.topic = topic
        self.wiki = Wikipedia(topic)
        self.hsw = Howstuffworks(topic)
        self.nyt = Nytimes(topic)
        # self.duck = Duckduckgo(topic)
        # self.goog = Google(topic)
        # self.youtube = Youtube(topic)

    def create_box(self):
        box = {"keyword": self.topic}
        sources = {
            'Wikipedia': self.wiki.get_summary,
            'HowStuffWorks': self.getHSWArticles,
            'NYTimes': self.getNYArticles,
            # 'DuckDuckGo': self.duck.getDefinition,
            # 'Google': self.getGoogleArticles,
            # 'GoogleImages': self.getImages,
            # 'YouTube': self.getYoutubeVideos,
        }
        for name, func in sources.items():
            try:
                box[name] = func()
            except Exception as exc:
                logmsg = "Error with topic {0} using {1}: {2}"
                logger.error(logmsg.format(self.topic, name, exc))
        return box

    def getHSWArticles(self):
        articles = []
        for i in range(4):
            article, blurb, headline = self.hsw.getArticle(), self.hsw.getBlurb(), self.hsw.getHeadline()
            if not all([article, blurb, headline]):
                return articles
            articles.append({"url": article, "headline": headline, "blurb": blurb})
        return articles

    def getNYArticles(self):
        articles = []
        for i in range(4):
            temp = self.nyt.getArticle()
            if not temp:
                return articles
            articles.append({"url": temp[0], "headline": temp[1], "blurb": temp[2]})
        return articles

    def getYoutubeVideos(self):
        videos = []
        if not self.youtube:
            return videos
        for i in range(4):
            temp = self.youtube.getVideo()
            if not temp:
                return videos
            videos.append({"url": temp[1], "title": temp[0]})
        return videos

    def getGoogleArticles(self):
        articles = []
        if not self.goog:
            return articles
        for i in range(4):
            temp = self.goog.getArticle()
            if not temp:
                return articles
            articles.append({"url": temp[1], "headline": temp[0], "blurb": temp[2]})
        return articles

    def getImages(self):
        images = [0]*4
        if not self.goog:
            return []
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
    for item in gen:
        print item
