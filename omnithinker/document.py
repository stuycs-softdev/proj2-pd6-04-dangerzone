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
        pass

    @property
    def summary(self):
        if len(self.text) < 500:
            return self.text
        return self.text[:497] + u"..."

    def render_txt(self):
        """Renders the document into a .txt file."""
        raise NotImplementedError()

    def render_pdf(self):
        """Renders the document into a .pdf file."""
        raise NotImplementedError()
