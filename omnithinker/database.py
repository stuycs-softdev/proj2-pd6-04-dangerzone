import hashlib
import sqlite3

from flask import Markup

from .document import Document

__all__ = ["Database"]

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 2

class Database(object):
    """Represents an Omnithinker database for storing users and documents."""

    def __init__(self, filename):
        self.filename = filename

    def _create(self, conn):
        """Creates a fresh database, assuming one doesn't exist."""
        with open(SCHEMA_FILE) as fp:
            script = fp.read()
        conn.executescript(script % {"version": SCHEMA_VERSION})

    def _execute(self, query, *args):
        """Execute a query, creating/updating the database if necessary."""
        with sqlite3.connect(self.filename) as conn:
            try:
                result = conn.execute("SELECT version FROM version")
                if result.fetchone()[0] < SCHEMA_VERSION:
                    self._create(conn)
            except sqlite3.OperationalError:
                self._create(conn)
            return conn.execute(query, args).fetchall()

    def _get_next_userid(self):
        """Return the next user ID in sequence."""
        result = self._execute("SELECT MAX(user_id) FROM users")
        return result[0][0] + 1 if result[0][0] else 1

    def _get_next_docid(self):
        """Return the next document ID in sequence."""
        result = self._execute("SELECT MAX(document_id) FROM documents")
        return result[0][0] + 1 if result[0][0] else 1

    def login(self, username, password):
        """Try to log in the user with the given username/password."""
        query = "SELECT user_password_hash FROM users WHERE user_name = ?"
        result = self._execute(query, username)
        if not result:
            return "Incorrect username or password."
        pwhash = result[0][0]
        if hashlib.sha256(password).hexdigest() != pwhash:
            return "Incorrect username or password."
        return None

    def register(self, username, email, password, securityq, securitya):
        """Try to register a new user."""
        query = "SELECT 1 FROM users WHERE user_name = ?"
        result = self._execute(query, username)
        if result:
            return "That username is taken."
        user_id = self._get_next_userid()
        pwhash = hashlib.sha256(password).hexdigest()
        self._execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", user_id,
                      username, email, pwhash, securityq, securitya)
        return None

    def get_documents(self, username):
        """Return a list of all documents associated with a given username."""
        query = """SELECT document_id, document_author, document_title,
                          document_text
                   FROM documents LEFT JOIN users ON document_author = user_id
                   WHERE user_name = ?"""
        result = self._execute(query, username)
        documents = []
        for row in result:
            documents.append(Document(*row))
        return documents

    def get_document(self, docid):
        """Return a document given its ID. Return None if it doesn't exist."""
        query = """SELECT document_id, document_author, document_title,
                          document_text
                   FROM documents WHERE document_id = ?"""
        result = self._execute(query, docid)
        return Document(*result[0]) if result else None

    def authorize_document(self, username, docid):
        """Return whether the given document was created by the given user."""
        query = """SELECT user_name FROM documents
                   LEFT JOIN users ON document_author = user_id
                   WHERE document_id = ?"""
        result = self._execute(query, docid)
        if not result:
            return False
        author = result[0][0]
        return author is None or author == username

    def create_document(self, username, topic=None):
        """Create a document for a user and return its ID."""
        docid = self._get_next_docid()
        if username:
            query = "SELECT user_id FROM users WHERE user_name = ?"
            userid = self._execute(query, username)[0][0]
        else:
            userid = -1  # Anonymous
        if topic:
            title = topic
            template = u'My project about <span class="keyword">{0}</span>...'
            text = template.format(Markup.escape(topic))
        else:
            title = text = None
        query = "INSERT INTO documents VALUES (?, ?, ?, ?)"
        self._execute(query, docid, userid, title, text)
        return docid

    def save_document(self, document):
        """Save a document to the database."""
        query = """UPDATE documents SET document_title = ?, document_text = ?
                   WHERE document_id = ?"""
        self._execute(query, document.title, document.text, document.docid)
