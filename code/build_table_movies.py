import psycopg2
from pymongo import MongoClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

mc = MongoClient()
mdb = mc['movies']
movie_info = mdb.movie_info

dbname = 'movies'
table_name = 'movie_info'

try:
    conn = psycopg2.connect(dbname=dbname, user='Wei')
except:
    conn = psycopg2.connect(dbname='postgres', user='Wei')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    c = conn.cursor()
    c.execute("CREATE DATABASE %s;" % dbname)
    conn.commit()
    conn.close()
    conn = psycopg2.connect(dbname=dbname, user='Wei')



c = conn.cursor()
c.execute("DROP TABLE IF EXISTS %s;" % table_name)
c.execute(
    """CREATE TABLE %s (
        id serial PRIMARY KEY, 
        imdb_id integer,
        year integer,
        title varchar, 
        box_office real,
        genre varchar,
        url varchar,
        image_url varchar,
        plot text
        );
    """ % table_name)

r = list(movie_info.find({},{'_id': 1, 'year': 1, 'title': 1, 'image_url': 1, 'genre': 1, 'BoxOffice': 1, 'Plot': 1, 'url': 1}))

c.executemany(
    """INSERT INTO movie_info (
        imdb_id,
        year,
        title,
        box_office,
        genre,
        url,
        image_url,
        plot
    )
    VALUES (
        %(_id)s,
        %(year)s,
        %(title)s,
        %(BoxOffice)s,
        %(genre)s,
        %(url)s,
        %(image_url)s,
        %(Plot)s
    )
    """, 
    r
    )

conn.commit()
conn.close()