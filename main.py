#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, abort
from urllib.parse import urlparse
import os
from urlshortener import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
            'index.html')

    elif request.method == 'POST':
        long_url = request.form['url']

        if urlparse(long_url).scheme == '':
            long_url = 'http://' + long_url

        saved_url = url_in_db(long_url)
        if saved_url == False:
            url_id = insert_new_url(long_url)
        else:
            url_id = saved_url

        encoded_url = dec_to_base(int(url_id))

        return render_template(
            'index.html',
            short_url=encoded_url
            )

@app.route('/1/<short_url>')
def redirect_url(short_url):
    decoded = to_base10(short_url)
    long_url = get_long_url(decoded)

    if long_url != False:
        return redirect(long_url)
    else:
        abort(404)

if __name__ == '__main__':
    if 'HEROKU_CHECK' in os.environ:
        app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT')))
    else:
        app.run(debug=True)

