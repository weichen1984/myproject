import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import cPickle as pkl


IMDbURL = "http://www.imdb.com"


def end_flag(txt):
    total = txt.split()
    cnts = total[0].split('-')
    n = len(cnts)
    if n == 1:
        return False, int(cnts[0])
    else:
        return cnts[1] != total[2], int(total[2].replace(',', ''))

def get_movie_list(year, start=1, count=100, country='us', ttype='feature'):
    print 'test'
    url = IMDbURL + '/search/title?' + \
          'countries=' + country + '&' + \
          'release_date=' + str(year) + '&' + \
          'title_type=' + ttype + '&' + \
          'start=' + str(start) + '&' + \
          'sort=' + 'moviemeter,asc' + '&' + \
          'count=' + str(count)
    r = requests.get(url)
    soup = BS(r.content, 'html.parser')


    # check if the current page is the final page for the year
    # if not, return False and the total number of query returns
    #   which means the total number of movies returned 
    # if yes, return True
    hit = soup.find('div', id='left')
    if hit != None:
        # print 'test1'
        txt = hit.text
        flag, cnt = end_flag(txt)
    else:
        # print 'test2'
        flag, cnt = False, 0

    # get all the movies in this page
    # imdb id, title, image_url
    titles = soup.find_all('td', class_='title')
    images = soup.find_all('td', class_='image')


    # check if an empty list if returned
    # this should not be a problem, just to double check
    ids = []
    tts = []
    img = []
    ttx = []
    imgs = []

    if titles:

        for x, y in zip(titles, images):
            # print 'test3'
            title = x.find('a')
            mid = title['href'].split('/')[-2].replace('tt','')
            m_title = title.text
            image = y.find('img')['src']
            ids.append(mid)  
            tts.append(m_title)
            img.append(image)
            ttx.append(str(x))
            imgs.append(str(y))


    df = pd.DataFrame({'id': ids, 'year': year, 'title': tts, 'image_url': img, 'title_text': ttx, 'image_text': imgs})
    return flag, cnt, df




def get_movie_list_per_year(year, country='us', ttype='feature'):
    start = 1
    count = 100
    flag = True
    df = pd.DataFrame({'id': [], 'year': [], 'title': [], 'image_url': [], 'title_text': [], 'image_text': []})
    while flag:
        print 'getting movies from %s from %s to %s' % (year, start, count)
        flag, cnt, dft = get_movie_list(year=year, start=start, count=count, country=country, ttype=ttype)
        start += count
        df = pd.concat([df, dft])
    print str(year) + ':', cnt
    return df


def get_movie(years, country='us', ttype='feature'):
    df = pd.DataFrame({'id': [], 'year': [], 'title': [], 'image_url': [], 'title_text': [], 'image_text': []})
    for year in years:
        print 'getting movies from', year
        dft = get_movie_list_per_year(year, country=country, ttype=ttype)
        df = pd.concat([df, dft])
        fn = '../data/movies' + str(year) + '.df'
        pkl.dump(dft, open(fn, 'wb'))
    return df


if __name__ == '__main__':
    # pass
    years = xrange(1874, 2015)
    df = get_movie(years)
    pkl.dump(df, open('../data/movies.df', 'wb'))




