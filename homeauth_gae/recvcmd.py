import webapp2,logging,json,datetime
#from google.appengine.api import users
from google.appengine.ext import db
import keymodel,cmdmodel
import keyverify
class MainPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        rescmd = []
        resmsg = {'err':'error','response':rescmd}
        try:
            enctext=eval(self.request.get('signature'))
            encinfo=eval(self.request.get('userinfo'))
        except Exception,data:
            logging.error(data)
            resmsg['err'] = data
        else:
            user = keyverify.verifyKey(enctext, encinfo)
            if user:
                resmsg['err'] = 'ok'
                cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1 ORDER BY mtime",user)
                for c in cmd:
                    rescmd.append({'cmd':c.cmd, 
                        'mtime':(c.mtime + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                        'etime':(c.etime + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                        'info':c.info,
                        'new':c.new,
                        'key':str(c.key())})
                    if c.new:
                        c.new = False
                        c.etime = datetime.datetime.utcnow()
                        c.put()
                resmsg['response'] = rescmd        
        self.response.write(json.dumps(resmsg))
    	
app=webapp2.WSGIApplication([('/recvcmd',MainPage)],
                            debug=True)
