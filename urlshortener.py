#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import string
import urllib
from urllib.parse import urlparse
import psycopg2

def dec_to_base(num):
    alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"
    base = len(alphabet)

    num, rem = divmod(num, base)
    result = alphabet[rem]
    while num:
        num, rem = divmod(num, base)
        result = alphabet[rem] + result
    return result

def to_base10(num):
    alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"

    return sum(alphabet.find(x)*len(alphabet)**i for i,x in enumerate(num))

def insert_new_url(url):
    conn = in_heroku()
    cur = conn.cursor()
    cur.execute('''INSERT INTO long_urls (url) VALUES ('%s') RETURNING id;''' % url)
    last_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return last_id

def get_long_url(url_id):
    conn = in_heroku()
    cur = conn.cursor()

    cur.execute('''SELECT url FROM long_urls WHERE id = '%s';''' % url_id)
    try:
        long_url = cur.fetchone()[0]
    except:
        long_url = False

    conn.commit()
    conn.close()

    return long_url

def url_in_db(url):
    conn = in_heroku()
    cur = conn.cursor()

    cur.execute('''SELECT id FROM long_urls WHERE url = '%s';''' % url)
    try:
        saved_url = cur.fetchone()[0]
    except:
        saved_url = False

    conn.commit()
    conn.close()

    return saved_url

def in_heroku():
    if 'DATABASE_URL' in os.environ and os.environ['DATABASE_URL']:
        urllib.parse.uses_netloc.append('postgres')
        url = urlparse(os.environ['DATABASE_URL'])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn
    else:
        conn = psycopg2.connect(database='urls')
        return conn

    return False
