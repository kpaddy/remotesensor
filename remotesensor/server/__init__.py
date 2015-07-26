import tornado.ioloop
import tornado.web
import json
import sys
import logging
import traceback
import pymongo
from tornado.options import define, options, parse_command_line
from remotesensor.database.sensorreadings import SensorReadingWriter
from remotesensor.database.outsidereadings import OusideReadingWriter
from remotesensor.database.userdb import UserDB
from pymongo import Connection
from pymongo.errors import ConnectionFailure
# logging.basicConfig(filename='/var/log/sensors/server.log',level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(ch)


define("port", default=12000, help="Run on the given port", type=int)

class Application(tornado.web.Application):
    # This portion of the application gets used to startup the settings,
    # this is part of the settings, and configurations
    def __init__(self):
        handlers = [
            (r"/sensor", SensorHandler),
            (r"/api", ApiHandler),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': "/Apps/workspaces_merge/remotesensor/remotesensor/webapp/ChartFiles/js"}),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': "/Apps/workspaces_merge/remotesensor/remotesensor/webapp/ChartFiles/css"}),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': "/Users/nthomas/Projects/remotesensor/remotesensor/webapp/"}),
            (r"/login", TwitterLoginHandler)
        ]
        settings = {
            "twitter_consumer_key": "B4LoarSuMS3Ltsex8TxBqjW8V",
            "twitter_consumer_secret": "0IJewHWXwjLn8peIneRirX7Bm9i69XnlcSfxVtkOFtrDbp7IHE",
            "login_url": "/auth/login",
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            #xsrf_cookies=True,
            "debug": True
        }

        tornado.web.Application.__init__(self, handlers, **settings)
        # try:
        #     self.con = Connection(host="localhost",port=27017)
        #     print "Connected Successfully"
        # except ConnectionFailure, e:
        #     sys.stderr.write("Could not connect to MongoDB: %s" %e)
        # self.db = self.con["user"]
        # assert self.db.connection == self.con


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(404)

    def post(self):
        self.send_error(404)

    def get_current_user(self):
        user = self.get_secure_cookie('trakr')
        if not user: return None
        return True

class ApiHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        logger.debug('Initalizing API Handler and connecting to mongo at localhost ')
        self._orw = OusideReadingWriter()
        #self._orw = OusideReadingWriter(hostname='54.85.111.126')

    def get(self):
        zipcode = self.get_argument("zipcode", None)
        print 'inside get ',zipcode
        if zipcode :
            #res = []
            #for r in self._orw.findByZip(zipcode):
            #    res.append({'zipcode':r['zipcode'], 'name':r['name'], 'temp':r['main']['temp']})
            self.write(tornado.escape.json_encode(self._orw.findByZip(zipcode)))
        else:
            self.set_status(500)
            self.write('INVALID REQUEST')

    def post(self):
        self.set_status(500)
        self.write('INVALID REQUEST')

class TwitterLoginHandler(tornado.web.RequestHandler,
                          tornado.auth.TwitterMixin):
    """Handling Twitter authentication for the remote sensor app"""

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        logger.debug('Initalizing TwitterLoginHandler and connecting to MongoDB at localhost ')
        self._user = UserDB()

    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            self.async_callback(self._on_auth(user))
            # return
        else:
            self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")

        # Saving user information to secure cookies
        self.set_secure_cookie('screen_name', user['access_token']['screen_name'])
        self.set_secure_cookie('user_id', user['access_token']['user_id'])
        self.set_secure_cookie('access_token_key', user['access_token']['key'])
        self.set_secure_cookie('access_token_secret', user['access_token']['secret'])

        logger.debug('Initalizing Sensor Handler and connecting to mongo at localhost ')

        # On successful authentication, check for valid user and then redirect to homepage
        if self.db.users.find_one({"screen_name" : user["screen_name"]}):
            self.redirect('/home')
        else:
            self.redirect('/login')

class LogoutHandler(MainHandler):
    def get(self):
        # This logs the user out of this demo app, but does not log them
        # out of Google.  Since Google remembers previous authorizations,
        # returning to this app will log them back in immediately with no
        # interaction (unless they have separately logged out of Google in
        # the meantime).
        self.clear_cookie("screen_name")
        self.clear_cookie("user_id")
        self.clear_cookie("access_token_key")
        self.clear_cookie("access_token_secret")
        self.redirect('/index.html')


class SensorHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        logger.debug('Initalizing Sensor Handler and connecting to mongo at localhost ')
        self._srw = SensorReadingWriter()
        #self._srw = SensorReadingWriter(hostname='54.85.111.126')

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
            if t < -25.00 or t > 110.00 :
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


if __name__ == "__main__":
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print 'starting at port: ', options.port
    tornado.ioloop.IOLoop.instance().start()
