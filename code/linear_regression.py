import dill
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.linear_model import Ridge
from sklearn.cross_validation import train_test_split

nids = dill.load(open('movie_ids.pkl', 'rb'))
model = dill.load(open('all2.pkl', 'rb'))
W = model.W
df = pd.DataFrame(W, index=nids)

c = MongoClient()
db = c['movies']
boxoffice2 = db.boxoffice2
movie_info = db.movie_info

r = list(boxoffice2.find({}, {'_id': 1, 'BoxOffice2': 1}))
df_bf = pd.DataFrame(r).set_index('_id')

r2 = list(movie_info.find({}, {'_id':1, 'year':1}))
df_year = pd.DataFrame(r2)
df_year = df_year.set_index('_id')


df = df.join(df_bf).join(df_year)

cond1 = (df['year'] >= 2010)
cond2 = ~ np.isnan(df['BoxOffice2'])

cond = cond1 & cond2

df_subset = df[cond]
y = df_subset['BoxOffice2'].values
df_subset.pop('BoxOffice2')
df_subset.pop('year')
X = df_subset.values

y = y / max(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
ridge = Ridge()
ridge.fit(X_train, y_train)
y = ridge.predict(X_test)
rsquare = ridge.score(X_test, y_test)





