'''
Created on May 26, 2015

@author: PaddyK
'''
from datetime import datetime

from remotesensor.database import MongoDBWriter
from remotesensor.sensors import Sensor
import time

class SensorManagement(MongoDBWriter):
    def __init__(self, dbname='sensors', collectionname='sensors', hostname='localhost'):
        MongoDBWriter.__init__(self, dbname, collectionname, hostname=hostname)
    
    def registerSensor(self, doc):
        if type(doc) != dict:
            doc = doc.__dict__
        if not doc.has_key('_id'):
            doc['_id'] = doc['id']
            doc['createdTime'] = datetime.now()
        self.saveToDb([doc])


    def findAll(self):
        table = self.client[self._dbname][self._collectionname]
        for row in table.find(): 
            print row
    '''
        Retreives temperature sensors for a given Customer
    '''
            
    def findByCustomer(self, customerId):
        table = self.client[self._dbname][self._collectionname]
        rows = []
        for row in table.find({"customerId":customerId}).sort("dt" ): 
            rows.append(row)
        return rows
        
class SensorReadingWriter(MongoDBWriter):
    
    def __init__(self, dbname='sensors', collectionname='readings', hostname='localhost'):
        MongoDBWriter.__init__(self, dbname, collectionname, hostname=hostname)

    '''
        Retreives all records
    '''
    def findAll(self):
        table = self.client[self._dbname][self._collectionname]
        for row in table.find(): 
            print row
        
    '''
        Retreives temperature readings for a given sensor
    '''
    def findBySensor(self, sensorid):
        table = self.client[self._dbname][self._collectionname]
        docs = []
        for row in table.find({"sensorid":sensorid}).sort("createdTime" ).limit(100): 
            row['createdTime'] = time.mktime(row['createdTime'].timetuple()) 
            #.strftime('%Y-%m-%dT%H:%M:%SZ')
            row['_id'] =  str(row['_id'])
            row['temperature'] = (row['temperature'] / 10000) * (9.0/5.0) + 32.0
            docs.append(row)
        return docs

    
    def saveReading(self, sensorid, temperature):
        doc = {}
        doc['sensorid'] = sensorid
        doc['temperature'] = temperature        
        doc['createdTime'] = datetime.now()
        self.saveToDb([doc])
        
if __name__ == '__main__':
    '''
    sw = SensorReadingWriter()
    records = [{'_id':{'sensorid':1231, 'dt':1432691988}, 'sensorid':1231, 'sensorname':'LOBBY', 'dt':1432691988, 'temp':68.33}, 
               {'_id':{'sensorid':1232, 'dt':1432691988}, 'sensorid':1232, 'sensorname':'CAFETERIA', 'dt':1432691988, 'temp':69.33}]
    #sw.saveToDb(records)
    #sw.findAll()
    sw.findBySensor(1231)
    s = Sensor()
    s.id = 11112
    s.customerId = 22222
    s.name  = 'LOBBY'
    s.zipcode  = 19426
    s.installedTime  = datetime.now()
    s.activatedTime  = datetime.now()
    s.currenStatus = 'ACTIVE'
    #sm = SensorManagement(hostname='54.85.111.126')
    #sm.registerSensor(s)x
    #sm.findAll()
    #sm.findByCustomer(22222)
    srw = SensorReadingWriter(hostname='54.85.111.126')
    #srw.saveReading(11112, 88.22 )
    print srw.findBySensor(1000)
    '''
    pass