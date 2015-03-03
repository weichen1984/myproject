from pymongo import MongoClient
import cPickle as pkl

c = MongoClient()
db = c['movies']
movie = db.movies

df = pkl.load(open('../data/movies.df'))
lst = df.to_dict('record')
ids = []
for x in lst:
    ids.append(movie.save(x))

