import os
import shutil
import cPickle as pickle

movies = pickle.load(open('../data/movies.df'))
fromdir = '/Users/Wei/Downloads/exp_eng/files/'
todir = '../data/opensubtitles/'

def cp_sub(year):
    cond1 = movies['year'] == year
    cond2 = movies['flag']
    cond = cond1 & cond2
    movie = movies[cond][['id', 'sub_id']]
    mids = movie['id'].values
    sids = movie['sub_id'].values
    outdir = todir + str(year) + '/'
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for mid, isid in zip(mids, sids):
        sid = int(isid)
        shutil.copy2(fromdir + str(sid) + '.gz', outdir)
        os.system('gunzip ' + outdir + str(sid) + '.gz')
        os.rename(outdir + str(sid), outdir + mid + '.srt')

def cp_subs(years):
    for year in years:
        print 'year = ', year
        cp.sub(year)

if __name__ == '__main__':
    cp_sub(2013)
