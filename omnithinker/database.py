import hashlib
import sqlite3

__all__ = ["Database"]

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 1

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

    def login(self, username, password):
        """Try to log in the user with the given username/password."""
        query = "SELECT user_password_hash FROM users WHERE user_name = ?"
        results = self._execute(query, username)
        if not results:
            return "Incorrect username or password."
        pwhash = results[0][0]
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
