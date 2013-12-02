__all__ = ["Document"]

class Document(object):
    """Represents a text document as understood by the server."""

    def __init__(self):
        self.docid = None
        self.title = None
        self.text = None

    @property
    def keywords(self):
        pass

    @property
    def summary(self):
        if len(self.text) < 500:
            return self.text
        return self.text[:497] + u"..."

    def save(self):
        """Saves the document to the database."""
        print "Saving document {0} with content {1}".format(repr(self.title),
                                                            repr(self.text))

    def render_txt(self):
        """Renders the document into a .txt file."""
        pass

    def render_pdf(self):
        """Renders the document into a .pdf file."""
        pass
