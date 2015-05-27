from pymongo import MongoClient
import urllib2
import json

'''
    This Class MongoDBWriter acts as a Database Access Object
    which abstracts all calls to MongoDB. 
    This class connects to a mongodb host. 
    During intialization it creates a database and collections for this application
'''
class MongoDBWriter(object):
    '''
        Constructor, that takes hostname as a parameter. 
    '''
    def __init__(self, dbname, collectionname, hostname = 'localhost'   ):
        self.client = MongoClient(hostname, 27017)
        if  not self.client[dbname]:
            self.client[dbname]
        if not self.client[collectionname]:
            self.client[collectionname].create_collection(collectionname)
        self._dbname = dbname
        self._collectionname = collectionname
    '''
        Saves a list of temperature reading to mongodb. 
    '''
    def saveToDb(self, docs):
        table = self.client[self._dbname][self._collectionname]
        table.insert(docs)
    