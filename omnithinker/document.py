from bs4 import BeautifulSoup
from flask import Markup

__all__ = ["Document"]

class Document(object):
    """Represents a text document as understood by the server."""

    def __init__(self, docid, author, title, text):
        self.docid = docid
        self.author = author
        self.title = title
        self.text = text

    @property
    def keywords(self):
        if not self.text:
            return []
        keywords = []
        soup = BeautifulSoup(self.text)
        for tag in soup.find_all("span", {"class": "keyword"}):
            keywords.append(tag.get_text())
        return keywords

    @property
    def summary(self):
        if not self.text:
            return None
        if len(self.text) < 500:
            return Markup(self.text).striptags()
        return Markup(self.text[:497]).striptags() + u"..."

    def render_txt(self):
        """Renders the document into a .txt file."""
        raise NotImplementedError()

    def render_pdf(self):
        """Renders the document into a .pdf file."""
        raise NotImplementedError()
