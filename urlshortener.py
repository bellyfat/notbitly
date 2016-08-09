#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import string
import psycopg2

def dec_to_base(num):
    alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"
    base = len(alphabet)

    if base <= 0:
        return 0
    num, rem = divmod(num, base)
    result = alphabet[rem]
    while num:
        num, rem = divmod(num, base)
        result = alphabet[rem] + result
    return result

def to_base10(num):
    alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"

    return sum(alphabet.find(x)*len(alphabet)**i for i,x in enumerate(num))


# create table long_urls (id SERIAL PRIMARY KEY, url TEXT NOT NULL);


def insert_new_url(url):
    conn = psycopg2.connect(database='urls')
    cur = conn.cursor()
    cur.execute('''INSERT INTO long_urls (url) VALUES ('%s') RETURNING id;''' % url)
    last_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return last_id

def get_long_url(url_id):
    conn = psycopg2.connect(database='urls')
    cur = conn.cursor()

    cur.execute('''SELECT url FROM long_urls WHERE id = '%s';''' % url_id)
    long_url = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return long_url
