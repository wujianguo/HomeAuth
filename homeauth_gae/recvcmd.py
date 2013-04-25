import webapp2,logging,json,datetime
from google.appengine.api import users
from google.appengine.ext import db
from Crypto.PublicKey import RSA
import keymodel,cmdmodel

class MainPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        rescmd = {'recvtime':None,'newcmd':[],'oldcmd':[]}
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
                cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1",user)
                cmd = cmd.get()
                if cmd:
                    rescmd['newcmd'] = cmd.newcmd
                    rescmd['oldcmd'] = cmd.oldcmd
                    rescmd['recvtime'] = cmd.last_recvcmd_time.strftime("%Y-%m-%d %H:%M:%S")
                    resmsg['response'] = rescmd
                    cmd.oldcmd.extend(cmd.newcmd)
                    cmd.newcmd = []
                    cmd.last_getcmd_time = datetime.datetime.utcnow()
                    cmd.put()
            else:
                resmsg['err'] = 'invalid data'
        else:
            resmsg['err'] = 'invalid user'

        
        self.response.write(json.dumps(resmsg))
    	

app=webapp2.WSGIApplication([('/recvcmd',MainPage)],
                            debug=True)
