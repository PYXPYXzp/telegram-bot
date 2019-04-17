from mongoengine import connect

def connect_mongo(username, password):
    connect(db='telegram_db', host='mongodb', username=username, password=password)