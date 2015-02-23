import requests
from bs4 import BeautifulSoup as BS

IMDbURL = "http://www.imdb.com"

def end_flag(text):
    total = text.split()
    return total[0].split('-')[1] != total[2]

def get_movie_list(year, start=1, count=100, country='us', ttype='feature'):
    url = IMDbURL + '/search/title?' + \
          'countries=' + country + '&' + \
          'release_date=' + str(year) + '&' + \
          'title_type=' + ttype + '&' + \
          'start=' + str(start) + '&' + \
          'sort=' + 'moviemeter,asc' + '&' + \
          'count=' + str(count)
    r = requests.get(url)
    soup = BS(r.content, 'html.parser')
    flag = end_flag(soup.find('div', id='left').text)
    

    return soup




def get_movie_list_per_year(year, country='us', ttype='feature'):
    i = 0
    count = 100
    while nleft <
    get_movie_list(year=year, )



