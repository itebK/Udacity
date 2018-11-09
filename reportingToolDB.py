# Database code for the DB reportingTool

import psycopg2

DBNAME = "news"

def get_most_three_popular_articles():
    """Return the most popular three articles of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        select title, views from
        (select substr(path, 10), count(*) as views from log where path !='/' group by path)
        as hits, articles where substr = slug order by views desc limit 3;
        """)
    return c.fetchall()
    db.close()

def get_most_popular_authors():
    """Return the most popular article authors of all time"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        select name, sum(views) as tot_views from
        (select name, author, title, views from
        (select substr(path, 10), count(*) as views from log
        where path !='/' group by path)
        as hits, articles, authors
        where substr = slug and author = authors.id
        order by views desc)
        as tables group by name order by tot_views desc;
        """)
    authors = c.fetchall()
    db.close()
    return authors
def get_error_days():
    """Return the most popular article authors of all time"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select requests.date, errors.http_404 * 100 / requests.http_requests::float from
                (select date_trunc('day', time) as date, count(*) as http_requests from log group by date) as requests,
                (select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date) as errors
                where requests.date = errors.date 
                and errors.http_404 * 100 / requests.http_requests::float > 0.1
                order by requests.date desc;""")
    errorLog = c.fetchall()
    db.close()
    return errorLog

