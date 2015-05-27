'''
Created on May 26, 2015

@author: PaddyK
'''
from datetime import datetime

from remotesensor.database import MongoDBWriter
from remotesensor.sensors import Sensor


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
        for row in table.find({"customerId":customerId}).sort("dt" ): 
            print row
        
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
        for row in table.find({"_id.sensorid":sensorid}).sort("dt" ): 
            print row

if __name__ == '__main__':
    '''
    sw = SensorReadingWriter()
    records = [{'_id':{'sensorid':1231, 'dt':1432691988}, 'sensorid':1231, 'sensorname':'LOBBY', 'dt':1432691988, 'temp':68.33}, 
               {'_id':{'sensorid':1232, 'dt':1432691988}, 'sensorid':1232, 'sensorname':'CAFETERIA', 'dt':1432691988, 'temp':69.33}]
    #sw.saveToDb(records)
    #sw.findAll()
    sw.findBySensor(1231)
    '''
    s = Sensor()
    s.id = 11112
    s.customerId = 22222
    s.name  = 'LOBBY'
    s.zipcode  = 19426
    s.installedTime  = datetime.now()
    s.activatedTime  = datetime.now()
    s.currenStatus = 'ACTIVE'
    sm = SensorManagement()
    #sm.registerSensor(s)
    #sm.findAll()
    sm.findByCustomer(22222)
    