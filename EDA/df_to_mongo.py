from pymongo import MongoClient
import cPickle as pkl

c = MongoClient()
db = c['movies']
movie = db.movies

df = pkl.load(open('../data/movies.df'))
df.to_dict('record')