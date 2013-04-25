import datetime
import webapp2
import keymodel,cmdmodel
from google.appengine.api import users
from google.appengine.ext import db
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))
class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        template_values = {
            'user': user,
            'cmd': None,
        }

        curuser=db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1",user)
        userinfo=curuser.get()
        if userinfo:
            template_values.update({'key':userinfo})
            cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1",user)
            cmd = cmd.get()
            if cmd:
                template_values.update({'cmd':cmd})
            else:
                cmd = cmdmodel.CmdInfos(user=user)
                cmd.put()
        else:
            newuser = keymodel.PubKeys(pubkey='',user=user)
            newuser.put()
            cmd = cmdmodel.CmdInfos(user=user)
            cmd.put()
        template = JINJA_ENVIRONMENT.get_template('newcmd.html')
        self.response.write(template.render(template_values))
    def post(self):
    	user = users.get_current_user()
    	cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1",user)
        cmd = cmd.get()
        if cmd:
            cmd.newcmd.append(self.request.get('newcmd'))
            cmd.last_recvcmd_time = datetime.datetime.utcnow()
            cmd.put()
        template_values = {
            'user': user,
            'cmd': cmd,
        }
        template = JINJA_ENVIRONMENT.get_template('newcmd.html')
        self.response.write(template.render(template_values))
#       	self.redirect('/newcmd')

app=webapp2.WSGIApplication([('/newcmd',MainPage)],
                            debug=True)
