from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer
import dill as pickle
from nltk.corpus import names, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer



wordnet = WordNetLemmatizer()
stemmer = SnowballStemmer("english")


class Movier(object):

    def __init__(self, 
                 kw_tfidf={}, 
                 kw_nmf={}, 
                 kw_kmeans={}):
        self.kw_tfidf = kw_tfidf
        self.kw_nmf = kw_nmf
        self.kw_kmeans = kw_kmeans
        # self.tokenizer = None
        self.tfidf = None
        self.nmf = None
        self.kmean = None
        self.top_words = {}
        

    def clean(self, docs):
        '''
        get rid of <> and {} tags, links (with and without)
        '''
        regex = re.compile('{\d+}|<.+?>|((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)')
        return [regex.sub(' ', doc) for doc in docs]


    def tokenize(self, doc):
        '''
        use NLTK RegexpTokenizer
        '''
        tokenizer = RegexpTokenizer("[\w'\.\-]{2,}\w")
        return [stemmer.stem(x) for x in tokenizer.tokenize(doc)]


    # def apply_tfidf(self, docs, **kwargs):
    #     '''
    #     apply scikit-learn tfidf 
    #     '''
    #     self.tfidf = TfidfVectorizer(**kwargs)
    #     X = self.tfidf.fit_transform(docs)
    #     return X



    # def apply_nmf(self, X, **kwargs):
    #     '''
    #     apply scikit-learn NMF
    #     '''
    #     self.nmf = NMF(**kwargs)
    #     W = self.nmf.fit_transform(X)
    #     H = self.nmf.components_
    #     return W, H

    # def apply_kmeans(X, **kwargs):
    #     '''
    #     apply scikit-learn K-Means
    #     '''
    #     self.kmeans = KMeans(**kwargs)
    #     y = self.kmeans.fit_transform(X)
        # return y

    def fit(self, docs):
        '''
        pipeline: clean, tokenize, tfidf, nmf, kmeans
        '''
        print 'cleaning raw docs ......'
        clean_docs = self.clean(docs)

        print 'running tfidf ......'
        if 'tokenizer' not in kw_tfidf:
            self.tfidf = TfidfVectorizer(tokenizer=self.tokenize, **self.kw_tfidf)
        else:
            self.tfidf = TfidfVectorizer(**self.kw_tfidf)
        self.X = self.tfidf.fit_transform(clean_docs)

        print 'running NMF ......'
        self.nmf = NMF(**self.kw_nmf)
        self.W = self.nmf.fit_transform(self.X)
        self.H = self.nmf.components_

        print 'running KMeans ......'
        self.kmeans = KMeans(**self.kw_kmeans)
        self.kmeans.fit(self.W)


    def top_n_words(self, n):
        '''
        find the top n frequent words for each feature
        '''
        if n in self.top_words:
            return self.top_words[n]
        else:
            self.top_words[n] = {}
            k = self.H.shape[0]
            words = np.array(self.tfidf.get_feature_names())
            for i in xrange(k):
                indices = np.argsort(self.H[i])[-1:(-n-1):-1]
                self.top_words[n][i] = list(words[indices])



    
    # def pickler(self, filename):
    #     pickle.dump(self, open(filename, 'w'))


# def main():








if __name__ == '__main__':
    # names_words = [x.lower() for x in names.words()]
    df = pd.read_csv('../data/txt/sub_text_2013.txt', delimiter='\t')
    docs = list(df.iloc[:, 1].values)
    kw_tfidf = {'max_df': 0.8, 'stop_words': 'english', 'min_df':10}
    kw_nmf = {'n_components': 100, 'max_iter': 300}
    kw_kmeans = {'n_clusters': 20}
    model = Movier(kw_tfidf=kw_tfidf, kw_nmf=kw_nmf, kw_kmeans=kw_kmeans)
    model.fit(docs)
    # model.pickler('model2013.pkl')
    pickle.dump(model, open('model2013_nmf100iter300_tokstem.pkl', 'w'))







