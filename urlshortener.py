#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import string
import urllib
from urllib.parse import urlparse
import psycopg2

alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"

def dec_to_base(num):
    base = len(alphabet)

    num, rem = divmod(num, base)
    result = alphabet[rem]
    while num:
        num, rem = divmod(num, base)
        result = alphabet[rem] + result
    return result

def base_to_dec(num):
    return sum(alphabet.find(x)*len(alphabet)**i for i,x in enumerate(num))

def connect_db():
    conn = database_connection()
    cur = conn.cursor()
    return conn, cur

def disconnect_db(conn, cur):
    conn.commit()
    conn.close()

def insert_new_url(url):
    try:
        conn, cur = connect_db()

        query = "INSERT INTO long_urls (url) VALUES (%s) RETURNING id;"
        data = (url, )
        cur.execute(query, data)

        try:
            last_id = cur.fetchone()[0]
        except:
            return False
        finally:
            disconnect_db(conn, cur)

        return last_id

    except:
        return False


def get_long_url(url_id):
    try:
        conn, cur = connect_db()

        query = "SELECT url FROM long_urls WHERE id = %s;"
        data = (url_id, )
        cur.execute(query, data)

        try:
            long_url = cur.fetchone()[0]
        except:
            return False
        finally:
            disconnect_db(conn, cur)

        return long_url

    except:
        return False


def url_in_db(url):
    try:
        conn, cur = connect_db()

        query = "SELECT id FROM long_urls WHERE url = %s;"
        data = (url, )
        cur.execute(query, data)

        try:
            saved_url = cur.fetchone()[0]
        except:
            return False
        finally:
            disconnect_db(conn, cur)

        return saved_url

    except:
        return False

def database_connection():
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
