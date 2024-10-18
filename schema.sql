CREATE TABLE book (
    isbn TEXT PRIMARY KEY,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    publisher TEXT NOT NULL,
    rented BOOLEAN NOT NULL,
    rentcount INTEGER DEFAULT 0
);

CREATE TABLE user(
    neptun TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    rentedbooks INTEGER DEFAULT 0
);