import os
import sys
import requests
import zipfile
from bs4 import BeautifulSoup as BS 
import cPickle as pickle
import pandas as pd
import numpy as np
import re
from pymongo import MongoClient
from string import punctuation



def download_file(url, mid, path):
    ''' Downloads and extracts the url content.

       :kwarg url: Contains the download link to raw data.

    '''
    response = requests.get(url, stream = True)
    with open('subtitle.zip', 'wb') as out_file:
        fsrc = response.raw
        size = response.headers.get("content-length")
        length = 16*1024
        while True:
            buf = fsrc.read(length)
            if not buf:
                break
            out_file.write(buf)
            sys.stdout.write("Downloaded " + str(os.path.getsize('subtitle.zip')/1024) + "kb of " + str(int(size)/1024) + " kb\r")
            sys.stdout.flush()
        print "\nDownload complete\nExtracting"
    del response
    try:
        zipf = zipfile.ZipFile('subtitle.zip')
        fns = zipf.namelist()
        for x in fns:
            if x[-4:] == '.srt':
                fn = x
                break
        fn = fns[0]
        zipf.extract(fn, path)
        zipf.close()
        if path[-1] != '/':
            path += '/'
        os.rename(path+fn, path+mid+'.srt')
        os.remove('subtitle.zip')
    except:
        print "* The subtitle file is not good to extract."
        return False
    return True

def check_exist(url):
    r = requests.get(url)
    soup = BS(r.content)
    del r
    td = soup.find('td', class_='a1')
    return td

def replace_special_characters(title):
    # chars = "*.?+#^"
    for c in punctuation:
        title = title.replace(c, ' ')
    return title


def find_alternative_link(movie_title, year, subtitle_language, wrong_year=False):
    # movies might have a different name
    title_query = '+'.join(movie_title.lower().split())
    query = "http://subscene.com/subtitles/title?q=" + title_query + '&l=' + subtitle_language
    r = requests.get(query)
    soup = BS(r.content)
    del r
    tags = soup.find_all('div', class_='title')
    # titles = np.array(soup.find_all(text=re.compile(movie_title)))
    titles = [x.text.strip() for x in tags]
    if wrong_year:
        title = movie_title + ' (' + str(year) +')'
        indices = np.where(titles == title)[0]
        if indices.any():
            index = indices[0]
            tag = tags[index]
            url = 'http://subscene.com' + tag.find('a')['href'] + '/' + subtitle_language
            if check_exist(url) != None:
                return True, url, 'Wrong year, but exact subtitles exist'
            else:
                return False, None, 'Page exists but no subtitles are available'
        else:
            return False, None, 'Wrong year, and no subtitles are available'
    else:
        for i, tt in enumerate(titles):
            if (movie_title in tt) & (str(year) in tt):
                tag = tags[i]
                url = 'http://subscene.com' + tag.find('a')['href'] + '/' + subtitle_language
                if check_exist(url) != None:
                    return True, url, 'Exact match does not exist, but alternative does'
                else:
                    return False, None, 'Alternative page exists but no subtitles are available'
        return False, None, 'No match found' # history: No subtitle



def find_link(movie_title, year, subtitle_language='english'):
    movie_title = replace_special_characters(movie_title)
    title_query = '-'.join(movie_title.lower().split())
    url = "http://subscene.com/subtitles/" + title_query + '/' + subtitle_language
    r = requests.get(url)
    if r.status_code == 200:
        soup = BS(r.content)
        del r
        td = soup.find('td', class_='a1')
        if td == None:
            print 'Page exists but no subtitles are available'
            return False, None, 'Page exists but no subtitles are available'
        else:
            web_year = int(soup.find('div', class_='header').find('ul').find('li').text.split()[1])
            if year in range(web_year-2, web_year+3):
                return True, url, 'Exact subtitles exist'
            else:
                print 'wrong year'
                return find_alternative_link(movie_title, year, subtitle_language, wrong_year=True)
    else:
        print 'scraping subtitle link fail'
        del r
        return find_alternative_link(movie_title, year, subtitle_language)

def get_download_link(url):
    r1 = requests.get(url)
    sp1 = BS(r1.content)
    td = sp1.find('td', class_='a1')
    a = td.find('a')
    surl = 'http://subscene.com' + a['href']
    r2 = requests.get(surl)
    sp2 = BS(r2.content)
    div = sp2.find('div', class_='download')
    download_url = 'http://subscene.com' + div.find('a')['href']
    return download_url


def fetch_missing_subtitle(years, outfile='test.df'):
    c = MongoClient()
    db = c['movies']
    missing = db.missing
    # data = pickle.load(open('../data/subscene_subtitles/missing_subtitles.dct'))
    movies = pickle.load(open('../data/movies.df'))
    fetched = os.listdir('../data/subscene_subtitles/')
    # dct = {}
    # ids = []
    # yrs = []
    # tts = []
    # flgs = []
    # dl_urls = []
    
    for year in years:
        count = 0
        outdir = '../data/subscene_subtitles/' + str(year)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        cond1 = movies['year'] == year
        cond2 = ~ movies['flag']
        cond = cond1 & cond2
        movie = movies[cond][['id', 'year', 'title', '_id']]
        nids = movie['_id']
        mids = movie['id']
        # yrs.extend(movie['year'])
        titles = movie['title']
        # ids.extend(mids)
        # tts.extend(titles)
        # flag = []
        # dl_url = []
        for nid, mid, title in zip(nids, mids, titles):
            count += 1
            
            # if mid + '.srt' not in fetched:
            if missing.find({'_id': nid}).count() == 0:

                print count
                dct = {'_id': nid, 'id': mid, 'year': year, 'title': title}
                flg, surl, comment = find_link(title, year)
                dct['comment'] = comment
                if flg:
                    url = get_download_link(surl)
                    # dl_url.append(url)
                    dct['download_url'] = url
                    dct['flag'] = download_file(url, mid, outdir)
                    # f.open
                else:
                    # flag.append(flg)
                    dct['flag'] = flg
                    # dl_url.append(np.nan)
            # else:
                # data[nid]
                # flag.append(True)
                # dl_url.append('yes')
                missing.save(dct)
        # flgs.extend(flag)
        # dl_urls.extend(dl_url)
    # df = pd.DataFrame({'id': ids, 'year': yrs, 'title': tts, 'flag': flg})
    # pickle.dump(df, open('../data/subscene_subtitles/' + outfile, 'wb'))
    # pickle.dump(data, open('../data/subscene_subtitles/missing_subtitles.dct', 'wb'))



if __name__ == '__main__':
    # fetch_missing_subtitle([2014])
    pass





