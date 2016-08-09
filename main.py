#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
from urllib.parse import urlparse
from urlshortener import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
            'index.html',
            short_url='')

    elif request.method == 'POST':
        long_url = request.form['url']
        if urlparse(long_url).scheme == '':
            long_url = 'http://' + long_url
        url_id = insert_new_url(long_url)
        encoded_url = dec_to_base(int(url_id))
        return render_template(
            'index.html',
            short_url='http://localhost:5000/'+encoded_url
            )

@app.route('/<short_url>')
def redirect_url(short_url):
    decoded = to_base10(short_url)
    print(decoded)
    long_url = get_long_url(decoded)
    return redirect(long_url)


if __name__ == '__main__':
      app.run(debug=True)

