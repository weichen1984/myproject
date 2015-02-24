import os
import sys
import requests
import zipfile
from bs4 import BeautifulSoup as BS 
import pickle

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
        zipf.extract(fn, path)
        if path[-1] != '/':
            path += '/'
        os.rename(path+fn, path+mid+'.srt')
        os.remove('subtitle.zip')
    except:
        print "* The subtitle file is not good to extract."
        return False
    return True


def find_link(mid):
    url = "http://www.opensubtitles.org/en/search/sublanguageid-eng/imdbid-" + mid
    r = requests.get(url)
    if r.status_code == 200:
        soup = BS(r.content)
        subs = soup.select('a[href^="/en/subtitleserve/sub/"]')
        return 'http://www.opensubtitles.org' + subs[0]['href']
    else:
        print 'scraping subtitle link fail'
        return False

def fetch_subtitle():
    ids = pickle.load(open('data/ids.pkl'))
    flag = []
    cnt = 0
    for i in ids:
        cnt += 1
        print cnt
        surl = find_link(i)
        if surl:
            flag.append(download_file(surl, i, 'data/subtitles'))
        else:
            flag.append(surl)
    pickle.dump(open('data/flag.pkl', 'wb'))


if __name__ == '__main__':
    fetch_subtitle()





