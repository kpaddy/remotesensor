
class Sensor(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        self.id= None
        self.customerId = None
        self.zipcode = None
        self.name = None
        self.installedTime = None
        self.activatedTime = None
        self.currenStatus = None
        self.createdTime = None
        self.lastDataReceviedTime = None

    def registerNew(self, doc):
        pass

    def unRegister(self, doc):
        pass    
    
