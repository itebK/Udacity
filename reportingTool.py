#!/usr/bin/env python2
from flask import Flask, request, redirect, url_for, Response
from reportingToolDB import *
import sys
import datetime

app = Flask(__name__)
# HTML template for the page
HT = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Reporting tool</title>
  </head>
  <body>
    <h1>Reporting tool</h1>
    <ul>
    %s
    </ul>
  </body>
</html>
'''
# HTML template for an individual item
IT = '''\
   <li>"%s" ----- %s views</li>
'''
ERR = '''\
  <li> {} - {} errors </li>
  '''


@app.route('/articles', methods=['GET'])
def popular_articles():
    posts = "".join(IT % (t, v) for t, v in get_most_three_popular_articles())
    html = HT % posts
    return html


@app.route('/authors', methods=['GET'])
def popular_authors():
    posts = "".join(IT % (au, v) for au, v in get_most_popular_authors())
    html = HT % posts
    return html


@app.route('/errors', methods=['GET'])
def errors():
    posts = "".join(ERR.format(d_f(d), str(round(e, 2))+"%") for d, e in e_d())
    html = HT % posts
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
