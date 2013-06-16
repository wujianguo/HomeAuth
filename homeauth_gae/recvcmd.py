import webapp2,logging,json,datetime
from google.appengine.api import users
from google.appengine.ext import db
from Crypto.PublicKey import RSA
import keymodel,cmdmodel

class MainPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
#        rescmd = {'recvtime':None,'newcmd':[],'oldcmd':[]}
        rescmd = []
        resmsg = {'err':'ok','response':rescmd}
        try:
            enctext=eval(self.request.get('signature'))
            encinfo=eval(self.request.get('userinfo'))
        except Exception,data:
            logging.error(data)
            resmsg['err'] = data
            self.response.write(json.dumps(resmsg))
            return
        import os
        pri = os.path.join(os.path.dirname(__file__),'private/id_rsa')
        with open(pri) as f:
            center_privkey = f.read()
        privkey=RSA.importKey(center_privkey)
        try:
            info=privkey.decrypt(encinfo)
            gmail=info[2:int(info[0:2])+2]
            msg=info[2+int(info[0:2]):]
            user=users.User(email=gmail)
            curuser=db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1",user)
            userinfo=curuser.get()
        except Exception,data:
            logging.error(data)
            resmsg['err'] = data
            self.response.write(json.dumps(resmsg))
            return
        
        if userinfo:
            pubkey=RSA.importKey(userinfo.pubkey)
            if pubkey.verify(msg,enctext):
                cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1 ORDER BY mtime",user)
                for c in cmd:
                    rescmd.append({'cmd':c.cmd, 
                        'mtime':(c.mtime + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                        'info':c.info,
                        'new':c.new})
                    if c.new:
                        c.new = False
                        c.etime = datetime.datetime.utcnow()
                        c.put()
                resmsg['response'] = rescmd
            else:
                resmsg['err'] = 'invalid data'
        else:
            resmsg['err'] = 'invalid user'

        
        self.response.write(json.dumps(resmsg))
    	

app=webapp2.WSGIApplication([('/recvcmd',MainPage)],
                            debug=True)
