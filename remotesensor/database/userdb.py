'''
    This Class UserDB acts as a Database Access Object
    which abstracts all calls to the user database in MongoDB.
    This class connects to a mongodb host.
'''

import json
import urllib2
import sys
import time
from datetime import datetime

from remotesensor.database import MongoDBWriter


class UserDB(MongoDBWriter):

    def __init__(self, dbname='user', collectionname='users', hostname='localhost'):
        MongoDBWriter.__init__(self, dbname=dbname, collectionname=collectionname, hostname=hostname)


    '''
        Retreives all users
    '''
    def findAll(self):
        table = self.client[self._dbname][self._collectionname]
        for row in table.find():
            print row
