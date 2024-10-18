CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    publisher TEXT NOT NULL,
    rented BOOLEAN NOT NULL,
    rentcount INTEGER DEFAULT 0,
    rented_by TEXT
);

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    neptun TEXT UNIQUE,
    name TEXT NOT NULL,
    rentedbooks INTEGER DEFAULT 0
);
