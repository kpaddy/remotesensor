'''
    This Class MongoDBWriter acts as a Database Access Object
    which abstracts all calls to MongoDB. 
    This class connects to a mongodb host. 
    During intialization it creates a database and collections for this application
'''

import json
import urllib2

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

    '''
        Retreives temperature readings for a given zipcode
    '''
    def findByZip(self, zipcode):
        table = self.client[self._dbname][self._collectionname]
        for row in table.find({"_id.zipcode":zipcode}).sort("dt" ): 
            print row


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
    

#treader = TemperatureReader()
#temps = treader.getCurrentTempAtZipcodes(["19426", "19422"])

#print datetime.fromtimestamp(data['dt']), data

dbwriter = OusideReadingWriter()
#dbwriter.saveToDb(temps)
dbwriter.findByZip( "19426")
#dbwriter.findAll(  )
