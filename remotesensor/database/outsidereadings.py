'''
    This Class MongoDBWriter acts as a Database Access Object
    which abstracts all calls to MongoDB. 
    This class connects to a mongodb host. 
    During intialization it creates a database and collections for this application
'''

import json
import urllib2
import sys
import time
from datetime import datetime, timedelta

from remotesensor.database import MongoDBWriter


class OusideReadingWriter(MongoDBWriter):
    
    def __init__(self, dbname='outsidetemp', collectionname='readings', hostname='localhost'):
        MongoDBWriter.__init__(self, dbname=dbname, collectionname=collectionname, hostname=hostname)
        
                        
    '''
        Retreives all records
    '''
    def findAll(self):
        table = self.client[self._dbname][self._collectionname]
        for row in table.find(): 
            print row
        return table.find()
    '''
        Retreives temperature readings for a given zipcode
    '''
    def findByZip(self, zipcode):
        table = self.client[self._dbname][self._collectionname]
        print self._dbname, self._collectionname
        ctime = datetime.now() - timedelta(days=30)
        thirydays = time.mktime(ctime.timetuple())
        res = []
        for row in table.find({ "$and" : [{"_id.zipcode":zipcode}, {"_id.dt":{"$gt": thirydays}}] }).sort("dt" ): 
        #for row in table.find({"_id.zipcode":zipcode}).sort("dt" ): 
            res.append(row)
        return res

newrecords = [{'zipcode':'19426', 'timestamp':'', 'temperature':94.33 }, 
              {'zipcode':'19422', 'timestamp':'', 'temperature':93.33 }
              ]

class TemperatureReader(object):
    def __init__(self, *args, **kwargs):
        self.url = "http://api.openweathermap.org/data/2.5/weather?units=imperial&q="
    def getCurrentTempAtZipcode(self, zipcode):
        response = urllib2.urlopen(self.url + zipcode)
        data = json.load(response)   
        data['zipcode'] = zipcode
        data['_id'] = {'zipcode':zipcode, 'dt':data['dt']}
        return data 

    def getCurrentTempAtZipcodes(self, zipcodes):
        temps = []
        for zipcode in zipcodes:
            temps.append(self.getCurrentTempAtZipcode(zipcode))
        return temps
'''
while True:
    try:
        print 'Current time: ', datetime.now()
        treader = TemperatureReader()
        temps = treader.getCurrentTempAtZipcodes(["19426", "19422"])
        dbwriter = OusideReadingWriter(hostname='54.85.111.126')
        dbwriter.saveToDb(temps)
        print 'going to sleep for 30 minutes'
        time.sleep(30*60)
        #dbwriter.findByZip( "19426")
    except:
        print sys.exc_info()
        print 'going to sleep for 30 minutes'
        time.sleep(30*60)
'''
'''
ctime = datetime.now() - timedelta(days=30)
print time.mktime(ctime.timetuple())

dbwriter = OusideReadingWriter(hostname='54.85.111.126')
temps = dbwriter.findByZip( "19426")
print temps
'''