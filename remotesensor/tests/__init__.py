from datetime import timedelta
import unittest

from remotesensor.database.outsidereadings import OusideReadingWriter
from remotesensor.database.sensorreadings import SensorReadingWriter, \
    SensorManagement
'''
    PyUnit test cases to regressly test the web application. 
'''
class OutsideTempTestCase(unittest.TestCase):
    def setUp(self):
        self.dbwriter = OusideReadingWriter(hostname='54.85.111.126', dbname='test_outsidetemp', collectionname='test_readings')
        
        
    def tearDown(self):
        #print 'tearing down'
        self.dbwriter.client[self.dbwriter._dbname][self.dbwriter._collectionname].remove({'id':5188948})
        self.dbwriter = None
        
        
    def testSavingOutsiteTempRecord(self):
        temp = { u'main': {u'pressure': 1001, u'humidity': 62, u'temp_max': 86, u'temp': 82.18, u'temp_min': 78.8}, u'clouds': 
                {u'all': 1}, u'name': u'Evansburg', u'zipcode': u'19426', u'coord': {u'lat': 40.18, u'lon': -75.43}, u'sys': {u'country': u'US',  
                u'sunset': 1436920212, u'message': 0.0114, u'type': 1, u'id': 2361, u'sunrise': 1436867086}, 
                u'weather': [{u'description': u'light rain', u'main': u'Rain', u'id': 500, u'icon': u'10d'}, {u'description': u'proximity thunderstorm', u'main': u'Thunderstorm', u'id': 211, u'icon': u'11d'}], u'cod': 200, u'base': u'cmc stations', 
            u'dt': 1438383324, u'_id': {u'dt': 1438383324, u'zipcode': u'19426'}, u'id': 5188948, u'wind': {u'speed': 3.24, u'deg': 240}}
        self.assertIsNone(self.dbwriter.saveToDb(temp))

    def testFindByZipCode(self):
        temp = { u'main': {u'pressure': 1001, u'humidity': 62, u'temp_max': 86, u'temp': 82.18, u'temp_min': 78.8}, u'clouds': 
                {u'all': 1}, u'name': u'Evansburg', u'zipcode': u'19426', u'coord': {u'lat': 40.18, u'lon': -75.43}, u'sys': {u'country': u'US',  
                u'sunset': 1436920212, u'message': 0.0114, u'type': 1, u'id': 2361, u'sunrise': 1436867086}, 
                u'weather': [{u'description': u'light rain', u'main': u'Rain', u'id': 500, u'icon': u'10d'}, {u'description': u'proximity thunderstorm', u'main': u'Thunderstorm', u'id': 211, u'icon': u'11d'}], u'cod': 200, u'base': u'cmc stations', 
            u'dt': 1438383324, u'_id': {u'dt': 1438383324, u'zipcode': u'19426'}, u'id': 5188948, u'wind': {u'speed': 3.24, u'deg': 240}}
        self.dbwriter.saveToDb(temp)
        rec = self.dbwriter.findByZip("19426")[0]
        self.assertDictEqual(rec['_id'], {'dt': 1438383324, 'zipcode': '19426'} )


class SensorRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.sensor = SensorManagement(hostname='54.85.111.126', dbname='test_sensors', collectionname='test_sensors')
        
        
    def tearDown(self):
        self.sensor.client[self.sensor._dbname][self.sensor._collectionname].remove({'id':'10000'})
        self.sensor = None
    def testRegisterSensor(self):
        newsensor = {'id':'10000', 'customerId':22222, 'name':'Lobby', 'zipcode':19426, 'currentStatus': 'ACTIVE'}
        self.assertIsNone(self.sensor.registerSensor(newsensor))

    def testFindByCustomer(self):
        newsensor = {'id':'10000', 'customerId':22222, 'name':'Lobby', 'zipcode':19426, 'currentStatus': 'ACTIVE'}
        self.sensor.registerSensor(newsensor)
        rec = self.sensor.findByCustomer(22222)[0]
        self.assertEqual(22222, rec['customerId'], "Customer ID not found.")
        
class SensorReadingWriterTestCase(unittest.TestCase):
    def setUp(self):
        self.sensor = SensorReadingWriter(hostname='54.85.111.126', dbname='test_sensors', collectionname='test_readings')
        
    def tearDown(self):
        self.sensor.client[self.sensor._dbname][self.sensor._collectionname].remove({'id':'10000'})
        self.sensor = None
    def testSaveReading(self):
        self.assertIsNone(self.sensor.saveReading('10000', 333122))

    def testFindBySensor(self):
        self.sensor.saveReading('10000', 333122)
        rec = self.sensor.findBySensor('10000')[0]
        self.assertEqual(91.4, rec['temperature'], "Temperature does not match.")
        

if __name__ == "__main__":
    newSuite = unittest.TestSuite()
    newSuite.addTest(unittest.makeSuite(OutsideTempTestCase))
    newSuite.addTest(unittest.makeSuite(SensorRegistrationTestCase))
    newSuite.addTest(unittest.makeSuite(SensorReadingWriterTestCase))
    unittest.main()
    #import time
    ##from datetime import datetime 
    #ctime = datetime.now() - timedelta(days=10)
    #print time.mktime(ctime.timetuple())
