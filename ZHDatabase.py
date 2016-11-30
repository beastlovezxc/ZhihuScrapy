import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.Zhihu

print(db.collection_names())
