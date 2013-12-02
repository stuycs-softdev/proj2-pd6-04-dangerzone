import sqlite3

__all__ = ["Database"]

class Database(object):
    """Represents an Omnithinker database for storing users and documents."""

    def __init__(self, filename):
        self.filename = filename

    def login(self, username, password):
        return "Incorrect username or password."
