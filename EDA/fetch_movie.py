import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
from imdb import IMDb




def end_flag(text):
    total = text.split()
    return total[0].split('-')[1] != total[2], \
           int(total[2].replace(',', ''))

def get_movie_list(year, start=1, count=100, country='us', ttype='feature'):
    IMDbURL = "http://www.imdb.com"
    url = IMDbURL + '/search/title?' + \
          'countries=' + country + '&' + \
          'release_date=' + str(year) + '&' + \
          'title_type=' + ttype + '&' + \
          'start=' + str(start) + '&' + \
          'sort=' + 'moviemeter,asc' + '&' + \
          'count=' + str(count)
    r = requests.get(url)
    soup = BS(r.content, 'html.parser')
    flag, cnt = end_flag(soup.find('div', id='left').text)
    titles = soup.find_all('td', class_='title')
    ids = []
    #dct = {'id': [], 'title': [], 'rating': [], 'genre': []}
    # dct = {'id': []}
    # ia = IMDb()
    i = 0
    for x in titles:
        i += 1
        print i
        title = x.find('a')
        mid = title['href'].split('/')[-2].replace('tt','')
        ids.append(mid)
        # dct['id'].append(mid)
        # movie = ia.get_movie(mid)
        # dct['title'].append(movie['canonical title'])
        # dct['rating'].append(movie['rating'])
        # dct['genre'].append(movie['genre'])   

    return flag, cnt, ids




def get_movie_list_per_year(year, country='us', ttype='feature'):
    start = 1
    count = 100
    flag = True
    ids = []
    while flag:
        flag, cnt, tids = get_movie_list(year=year, start=start, count=count)
        start += count
        ids.extend(tids)
    return ids





