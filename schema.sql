-- Database schema
-- version 4

DROP TABLE IF EXISTS version;
CREATE TABLE version (
    version INTEGER
);
INSERT INTO version VALUES (%(version)s);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT,
    user_email TEXT,
    user_password_hash BLOB,
    user_security_question TEXT,
    user_security_answer BLOB
);

DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    document_author INTEGER,
    document_title TEXT,
    document_text TEXT,
    document_deleted BOOLEAN
);

DROP TABLE IF EXISTS locks;
CREATE TABLE locks (
    lock_id INTEGER PRIMARY KEY
);
