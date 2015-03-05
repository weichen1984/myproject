import requests
from pymongo import MongoClient


c = MongoClient()
db = c['movies']

# opensub = db.opensub
# cursor = opensub.find({'flag':True}, {'_id':1, 'id':1})

missing = db.missing
cursor = missing.find({'flag':True}, {'_id':1, 'id':1})

omdb = db.omdb
for x in cursor:
    nid = x['_id']
    if omdb.find({'_id': nid}).count() == 0:
        url = "http://www.omdbapi.com/?i=tt" + x['id'] + "&plot=full&r=json&tomatoes=true"
        response = requests.get(url)
        if response.status_code == 200:
            item = response.json()
            item['_id'] = nid
            item['id'] = x['id']
            item['flag'] = True
            omdb.save(item)
        else:
            item['_id'] = nid
            item['id'] = x['id']
            item['flag'] = False
            omdb.save(item)
        del response





