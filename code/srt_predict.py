import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dill as pickle
import sys
import os
import io
import chardet
import rarfile
import shutil
from movier2 import Movier

def check_text(line):
    '''
    check if each line of srt file is text
    '''
    line = line.strip()
    if '-->' in line or line == '':
        return ''
    else:
        line = line.encode('ascii', 'ignore')
        if line.isdigit():
            return ''
        else:
            return ' '.join(line.split())


def extract_text(fn, encoding):
    '''
    extract text from srt with the encoding
    '''
    tt = []
    with io.open(fn, 'r', encoding=encoding) as g:
        lines = g.readlines()
        for x in lines:
            y = check_text(x)
            if y:
                tt.append(y)
        text = ' '.join(tt).strip()
    return text


def extract_file(fn):
    '''
    extract text from srt file
    '''
    try:
        f = open(fn)
        content = f.read()
        f.close()
        r = chardet.detect(content)
        charenc = r['encoding']
        text = extract_text(fn, charenc)
    except:
        charenc = None
        text = extract_text(fn, charenc)

    return text



def main(fn):
    text = extract_file(fn)
    print x
    pass

if __name__ == '__main__':
    # fn = sys.argv[1]
    # main(fn)
    a = Movier()
    fn = '0111161.srt'
    text = extract_file(fn)
    text = ' '.join(a.tokenize(a.clean([text])[0]))
    model = pickle.load(open('random40_onlyw.pkl', 'rb'))
    years = pickle.load(open('random40_years.pkl', 'rb'))['year'].values
    n = len(years)
    # topics = ['Topic' + str(x) for x in xrange(1, n+1)]
    X = model.tfidf.transform([text])
    W = model.nmf.transform(X)
    ic = model.kmeans.predict(W)
    ic2 = model.kmeans2.predict(X)
    df = pd.DataFrame(model.W)
    df['year'] = years
    trends = df.groupby('year').sum() / df.groupby('year').count()
    model.top_n_words(50)
    indices = list(np.argsort(W)[0][::-1][:10])
    trend = trends.loc[:, indices]
    trend.plot(x=trend.index, kind='bar', subplots=True, layout=(4,3))
    for i, ind in enumerate(indices):
        print 'Topic %s: ' % ind
        print 'Top Words %s: ' % model.top_words[50][ind][:20]



