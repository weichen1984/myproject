import requests
from bs4 import BeautifulSoup as BS

IMDbURL = "http://www.imdb.com"

def get_movie_list(year, start=1, count=100, country='us', ttype='feature'):
    url = IMDbURL + '/search/title?' + \
          'country=' + country + '&' + \
          'release_date=' + str(year) + '&' + \
          'title_type=' + ttype + '&' + \
          'start=' + str(start) + '&' + \
          'sort=' + 'moviemeter,asc' + '&' + \
          'count=' + str(count)
    r = requests.get(url)
    soup = BS(r.content, 'html.parser')
    return soup


