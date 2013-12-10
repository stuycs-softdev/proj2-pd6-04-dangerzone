import json
import random
import urllib

API_URL = "http://en.wikipedia.org/w/api.php"
EXCLUSIONS = ["stub", "list", "disambig"]

random.seed(1337)  # Get consistent "random" boxes each time

class Wikipedia(object):
    def __init__(self, topic):
        self.topic = topic
        self.result_title = None

    def get_summary(self):
        """Return a string about a sentence or two long."""
        data = {"action": "query", "list": "search", "srlimit": 1,
                "format": "json", "srsearch": self.topic}
        raw = urllib.urlopen(API_URL, urllib.urlencode(data)).read()
        res = json.loads(raw)
        results = res["query"]["search"]
        if not results:
            return None
        self.result_title = title = results[0]["title"]
        snippet = results[0]["snippet"]
        if "REDIRECT" in snippet:
            return None
        return {"title": title, "snippet": snippet}

    def get_related_topics(self):
        """Return a list of topic strings related to the given topic."""
        if not self.result_title:
            return []
        cats, links = self._get_categories(), self._get_links()
        random.shuffle(cats)
        random.shuffle(links)
        results = cats + links[:5]
        topics = []
        for title in results:
            if not any([exclude in title.lower() for exclude in EXCLUSIONS]):
                topics.append(title)
        return topics[:10]

    def _get_categories(self):
        """Use prop=categories to get some topics."""
        data = {"action": "query", "prop": "categories", "clshow": "!hidden",
                "cllimit": 500, "format": "json", "titles": self.result_title}
        raw = urllib.urlopen(API_URL, urllib.urlencode(data)).read()
        res = json.loads(raw)
        page = res["query"]["pages"].values()[0]
        if "categories" not in page:
            return []
        return [cat["title"].split(":", 1)[1] for cat in page["categories"]]

    def _get_links(self):
        """Use prop=links to get some topics."""
        data = {"action": "query", "prop": "links", "plnamespace": "0",
                "pllimit": 500, "format": "json", "titles": self.result_title}
        raw = urllib.urlopen(API_URL, urllib.urlencode(data)).read()
        res = json.loads(raw)
        page = res["query"]["pages"].values()[0]
        if "links" not in page:
            return []
        return [link["title"] for link in page["links"]]

if __name__ == "__main__":
    def process(topic, depth, done):
        if depth > 2 or topic.lower() in done:
            return
        done.append(topic.lower())
        wiki = Wikipedia(topic)
        print topic, wiki.get_summary()
        for topic in wiki.get_related_topics():
            process(topic, depth + 1, done)
    process("apples", 0, [])
