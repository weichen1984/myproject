from pymongo import MongoClient
from bs4 import BeautifulSoup as BS
import numpy as np

c = MongoClient()

db = c['movies']
opensub = db.opensub
missing = db.missing
omdb = db.omdb
movie_info = db.movie_info


def get_genre(html):
    soup = BS(html, 'html.parser')
    try:
        return [x.strip() for x in soup.find_all('span', class_='genre')[0].text.split('|')]
    except:
        print 'no genre class'
        return None

def get_boxoffice(text):
    if text == 'N/A':
        return None
    else:
        text = text.strip('$')
        if 'M' in text:
            return 1000000 * float(text.replace('M', ''))
        elif 'k' in text:
            return 1000 * float(text.replace('k', ''))
        else:
            return float(text)

def add_opensub():
    r = opensub.find({'flag': True})
    # keys = ['_id', 'id', 'year', 'title', 'image_text', 'title_text', 'image_url']
    for x in r:
        y = x.copy()
        y.pop('flag')
        y.pop('sub_id')
        y['url'] = 'http://www.imdb.com/title/tt' + y['id'] + '/'
        y['genre'] = get_genre(y['title_text'])
        movie_info.save(y)

def add_subscene():
    r = missing.find({'flag': True})
    for x in r:
        # y = {}
        # keys = ['_id', 'id', 'year', 'title', 'image_text', 'title_text', 'image_url']
        nid = x['_id']
        y = opensub.find_one({'_id': nid}).copy()
        y.pop('flag')
        y.pop('sub_id')
        y['url'] = 'http://www.imdb.com/title/tt' + y['id'] + '/'
        y['genre'] = get_genre(y['title_text'])
        movie_info.save(y)

def add_omdb_info():
    r = omdb.find({}, {'_id': 1, 'Plot': 1, 'BoxOffice': 1})
    for x in r:
        nid = x['_id']
        query = {'$set': {'Plot': x['Plot'], 'BoxOffice': get_boxoffice(x['BoxOffice'])}}
        movie_info.update({'_id': nid}, query)

def main():
    add_opensub()
    add_subscene()
    add_omdb_info()

if __name__ == '__main__':
    main()

