from flask import Flask, request, redirect, url_for, Response
from reportingToolDB import *
import sys
import datetime


app = Flask(__name__)

# HTML template for the page
HTML_WRAP = '''\
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
ITEM = '''\
   <li>"%s" ----- %s views</li>
'''
ITEMERROR = '''\
  <li> {} --- {} %.errors </li>
  '''

@app.route('/articles', methods=['GET'])
def popular_articles():
    posts = "".join(ITEM %  (title,views) for title, views in get_most_three_popular_articles())
    html = HTML_WRAP % posts
    return html
@app.route('/authors', methods=['GET'])
def popular_authors():
    posts = "".join(ITEM % (authoName, t_views) for authoName, t_views in get_most_popular_authors())
    html = HTML_WRAP % posts
    return html
@app.route('/errors', methods=['GET'])
def errors():
    posts = "".join(ITEMERROR.format(  str(date).split(' ',1)[0], round(err,2) ) for date, err in get_error_days())
    html = HTML_WRAP % posts
    return html

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)