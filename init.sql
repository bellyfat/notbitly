CREATE DATABASE urls;
\c urls;
CREATE TABLE long_urls (id SERIAL PRIMARY KEY, url TEXT NOT NULL);
CREATE INDEX urls_idx ON long_urls (id, url);
