import pandas as pd
import numpy as np
import cPickle as pkl

df_movies = pkl.load(open('../data/movies.df'))
df_subtitles = pd.read_csv('../data/export.txt', delimiter='\t')
df = df_subtitles[['IDSubtitleFile', 'MovieImdbID']]
df = df.groupby('MovieImdbID').min()
movie_with_subs = set(df.index)
cond = df_movies['id'].astype(int).isin(movie_with_subs)
df_movies['flag'] = cond
df_movies['sub_id'] = np.nan
df_movies.loc[cond, 'sub_id'] = df.loc[df_movies[cond]['id'].astype(int)].values

pkl.dump(df_movies, open('../data/movies.df', 'wb'))