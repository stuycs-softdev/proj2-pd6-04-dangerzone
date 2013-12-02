-- Database schema
-- version 1

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
