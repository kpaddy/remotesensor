import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.httpserver
import json
import logging
import traceback
import pymongo
from datetime import datetime
from tornado.options import define, options, parse_command_line
from remotesensor.database import MongoDBWriter
from remotesensor.database.sensorreadings import SensorReadingWriter
from remotesensor.database.outsidereadings import OusideReadingWriter
from remotesensor.database.userdb import UserDB
from pymongo.errors import ConnectionFailure
# logging.basicConfig(filename='/var/log/sensors/server.log',level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(ch)

APPPATH = '/home/ubuntu/apps/remotesensor'
#APPPATH = '/python/git/remotesensornt/remotesensor/'


define("port", default=12000, help="Run on the given port", type=int)

'''
    A tornado Applicaton Router that routes incomming http requests to it's
    appropriate Tornado Handlers.
'''
class Application(tornado.web.Application):
    # This portion of the application gets used to startup the settings,
    # this is part of the settings, and configurations
    def __init__(self):
        handlers = [
            (r"/sensor", SensorHandler),
            (r"/", MainHandler),
            (r"/auth/login/", LoginHandler),
            (r"/auth/logout/", LogoutHandler),
            (r"/auth/twitter/", TwitterLoginHandler),
            (r"/user/register/", UserRegistrationHandler),
            (r"/sensor/register/", SensorRegistrationHandler),
            (r"/api", ApiHandler),
            (r'/js/(.*)', tornado.web.StaticFileHandler,
             {'path': APPPATH + "/webapp/ChartFiles/js"}),
            (r'/css/(.*)', tornado.web.StaticFileHandler,
              {'path': APPPATH + "/webapp/ChartFiles/css"}),
            (r"/sensor/view/", tornado.web.StaticFileHandler,
             {'path': APPPATH + "/webapp/Chart.html"}),
            (r"/(.*)", tornado.web.StaticFileHandler,
             {'path': APPPATH + "/webapp/"}),
            (r"/images/(.*)", tornado.web.StaticFileHandler,
             {'path': APPPATH + "/webapp/images"})
        ]
        settings = {
            "twitter_consumer_key": "B4LoarSuMS3Ltsex8TxBqjW8V",
            "twitter_consumer_secret": "0IJewHWXwjLn8peIneRirX7Bm9i69XnlcSfxVtkOFtrDbp7IHE",
            "login_url": "/auth/login/",
            "cookie_secret": "L8LwECiNRxqjnj82bjbz9snkMZlrpmuMEimlydNX/vt1LM=",
            # template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # "static_path": os.path.join(os.path.dirname(__file__), "static"),
            #xsrf_cookies=True,
            "debug": True
        }

        tornado.web.Application.__init__(self, handlers, **settings)
        ''' try:
            self.con = pymongo.Connection(host="localhost", port=27017)
            print "Connected Successfully"
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s"%e)
        self.db = self.con["user"]
        assert self.db.connection==self.con '''

'''
    The Default Tornado Handler 
'''
class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        if not self.current_user:
            self.redirect("/home.html")
            return
        username = self.current_user
        self.write('Hi there, ' + username)

'''
    This Tornado Handler handles all data API calls that are requested from the 
    Charts page. 
'''
class ApiHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        logger.debug('Initalizing API Handler and connecting to mongo at localhost ')
        self._orw = OusideReadingWriter()
        self.srw = SensorReadingWriter()
    def get(self):
        zipcode = self.get_argument("zipcode", None)
        print 'inside get ',zipcode
        if zipcode :
            outside = self._orw.findByZip(zipcode)
            sensorr = self.srw.findBySensor(1000)  
            self.write(tornado.escape.json_encode({'outside':outside, 'sensor':sensorr}))
        else:
            self.set_status(500)
            self.write('INVALID REQUEST')
    def post(self):
        self.set_status(500)
        self.write('INVALID REQUEST')

'''
    A tornado Handler to handle Logins. 
'''
class LoginHandler(MainHandler):
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.set_cookie("screen_name", self.get_argument("username", ""))
            self.redirect("/partials/home.html")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect("/partials/login.html")

    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render('/partials/login.html', errormessage = errormessage)

    def check_permission(self, password, username):
        if username == password:
            return True
        else:
            return False

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

'''
    This Tornado Handler handles all web requests related to Twitter OAuth.
'''
class TwitterLoginHandler(tornado.web.RequestHandler,
                          tornado.auth.TwitterMixin):
    """Handling Twitter authentication for the remote sensor app"""

    # def __init__(self, application, request, **kwargs):
    #     tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
    #     logger.debug('Initalizing TwitterLoginHandler and connecting to MongoDB at localhost ')
    #     self._user = UserDB()

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(callback=self._on_auth)
            return
        self.authenticate_redirect()

    @tornado.web.asynchronous
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")

        # Saving user information to secure cookies
        self.set_cookie('screen_name', user['access_token']['screen_name'])
        self.set_cookie('user_id', user['access_token']['user_id'])
        self.set_secure_cookie('access_token_key', user['access_token']['key'])
        self.set_secure_cookie('access_token_secret', user['access_token']['secret'])

        logger.debug('Initalizing Sensor Handler and connecting to mongo at localhost ')

        # On successful authentication, check for valid user and then redirect to homepage
        # Also saves the current datetime of login
        client = pymongo.MongoClient('localhost', 27017)
        user_db = client.user
        users = user_db.users
        if users.find_one({"screen_name": user['access_token']['screen_name']}):
            logger.debug("Found valid user")
            user_log_record = {"screen_name": user['access_token']['screen_name'],
                               "login_time": datetime.now()}
            user_log = user_db.user_log
            user_log.insert(user_log_record)
            self.redirect("/partials/home.html")
        else:
            logger.debug("No valid user found")
            self.redirect('/partials/login.html')


class LogoutHandler(MainHandler):
    def get(self):
        # This logs the user out of this app, but does not log them out of Twitter.
        self.clear_cookie("user")
        self.clear_cookie("screen_name")
        self.clear_cookie("user_id")
        self.clear_cookie("access_token_key")
        self.clear_cookie("access_token_secret")
        self.redirect("/home.html")

'''
    A Tornado Handler to handle all web requests related to User Registration. 
'''
class UserRegistrationHandler(MainHandler):
    def post(self):
        screen_name = self.get_argument("screen_name", "")
        name = self.get_argument("name", "")
        client = pymongo.MongoClient('localhost', 27017)
        user_db = client.user
        users = user_db.users
        if users.find_one({"screen_name": screen_name}):
            logger.debug("Error: Existing user")
            self.render('/partials/register_user.html', errormessage = "Error: Existing user")
        else:
            new_user = {"screen_name": screen_name,
                    "name": name,
                    "profile_image_url" : "",
                    "created_date": datetime.now()}
            users.insert(new_user)
            print "Added new user"
            self.redirect("/partials/register_user.html")

    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render('/partials/register_user.html', errormessage = errormessage)


'''
    A Tornodao Handler class that is used to save Sensor Readings. This api 
    is called directly from the ESP8266 Wifi Module. 
'''
class SensorHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        logger.debug('Initalizing Sensor Handler and connecting to mongo at localhost ')
        self._srw = SensorReadingWriter()
    def get(self):
        sensorid = self.get_argument("sensorid", None)
        if sensorid :
            self.write(tornado.escape.json_encode(self._srw.findBySensor(int(sensorid))))
        else:
            self.set_status(500)
            self.write('INVALID REQUEST')
            
    def post(self):
        data_json = None
        indata = None
        try:
            indata = tornado.escape.utf8(self.request.body)
            data_json = json.loads(indata)
        except:
            logger.error(traceback.format_exc()+'\ninput data is ' + indata)
            self.set_status(500)
            self.write('FAILED TO PARSE INPUT DATA')
        try:
            sensorid = data_json['id']
            t = data_json['t']
            if t < 200000 or t > 360000 :
                self.set_status(500)
                logger.error('Wrong temperature value => {} from sensor {} ' .format(t, sensorid))
                return self.write('Wrong temperature value =>' +  str(t))
            self._srw.saveReading(data_json['id'], data_json['t'])
        except:
            logger.error(traceback.format_exc() + '\ninput data is ' + indata)
            self.set_status(500)
            self.write('FAILED TO SAVE')
            return
        logger.debug( "saved Temperature" + str(data_json) )
        self.write('SUCCESS')

'''
    A Tornodao Handler class that is used to handle are request to register a Sensor. 
'''
class SensorRegistrationHandler(MainHandler):
    '''
        This method throws an error if the sensor already exists. Other wise creates a new record. 
    '''
    def post(self):
        name = self.get_argument("sensor_name", "")
        zipcode = self.get_argument("location", "")
        client = pymongo.MongoClient('localhost', 27017)
        sensor_db = client.sensor
        sensor_collection = sensor_db.sensor
        if sensor_collection.find_one({"name": name, "zipcode": zipcode}):
            logger.debug("Error: Existing sensor")
            self.render('/partials/register_sensor.html', errormessage = "Error: Existing sensor")
        else:
            new_sensor = {"name": name,
                    "customerId" : self.get_cookie("screen_name"),
                    "zipcode": zipcode,
                    "currentStatus": "ACTIVE",
                    "installedTime": datetime.now()}
            sensor_collection.insert(new_sensor)
            print "Added new sensor"
            self.redirect("/partials/register_sensor.html")

    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render('/partials/register_user.html', errormessage = errormessage)

'''
    This is the main code to run our application as a Web Server.
'''
if __name__ == "__main__":
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print 'starting server at port: ', options.port
    tornado.ioloop.IOLoop.instance().start()
