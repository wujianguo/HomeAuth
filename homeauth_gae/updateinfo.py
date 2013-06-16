import webapp2,logging,json,datetime
from google.appengine.ext import db
import keymodel,cmdmodel
import keyverify
class MainPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        resmsg = {'err':'error'}
        try:
            enctext=eval(self.request.get('signature'))
            encinfo=eval(self.request.get('userinfo'))
            strkey = self.request.get('key')
            logging.debug(strkey)
            cmdinfo = self.request.get('cmdinfo')
        except Exception,data:
            logging.error(data)
            resmsg['err'] = data
        else:
            if keyverify.verifyKey(enctext, encinfo):
                k = db.Key(encoded=strkey)
                cmd = db.get(k)
                if cmd:
                    cmd.info = cmdinfo
                    cmd.put()
                    resmsg['err'] = 'ok'
                else:
                    logging.warn('cmd none')
            else:
                logging.error('verifyKey error')
        self.response.write(json.dumps(resmsg))    

app=webapp2.WSGIApplication([('/updateinfo',MainPage)],
                            debug=True)
