SELECT *
FROM pg_extension;
create extension if not exists pgcrypto;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password text,
    salt text
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE nominees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    nominee_id INTEGER NOT NULL,
    voter_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (nominee_id) REFERENCES nominees (id)
);


