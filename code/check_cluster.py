import dill
import pandas as pd
import numpy as np
from pymongo import MongoClient

nids = dill.load(open('movie_ids.pkl', 'rb'))
model = dill.load(open('all2.pkl', 'rb'))

c = MongoClient()
db = c['movies']
movie_info = db.movie_info
r = list(movie_info.find({}, {'_id':1, 'title':1, 'year':1, 'genre':1, 'BoxOffice':1}))
df = pd.DataFrame(r)
df = df.set_index('_id').loc[nids]

boxoffice2 = db.boxoffice2
r2 = list(boxoffice2.find({}, {'_id': 1, 'BoxOffice2': 1}))
df_bf = pd.DataFrame(r2).set_index('_id')

df = df.join(df_bf)
df['label'] = model.kmeans.labels_


n_labels = len(df['label'].unique())
genres = []
for x in df['genre']:
    if x:
        genres.extend(x)
genres = list(set(genres))
n_genres = len(genres)
df_check = pd.DataFrame(np.zeros((n_labels, n_genres)), index=range(n_labels), columns=genres)
for nid in nids:
    label = df.loc[nid, 'label']
    genre = df.loc[nid, 'genre']
    if genre:
        for x in genre:
            df_check.loc[label, genre] += 1

