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

        curuser = db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1",user)
        if curuser:
            cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1 ORDER BY mtime",user)
#            cmd.order("-mtime")
            template_values.update({'cmd':cmd})
        else:
            newuser = keymodel.PubKeys(pubkey='',user=user)
            newuser.put()
        template = JINJA_ENVIRONMENT.get_template('newcmd.html')
        self.response.write(template.render(template_values))

    def post(self):
    	user = users.get_current_user()
        curuser = db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1", user)
        if not curuser:
            newuser = keymodel.PubKeys(pubkey = '', user = user)
            newuser.put()
        newcmd = cmdmodel.CmdInfos(user = user, cmd = self.request.get('newcmd'),
            mtime = datetime.datetime.utcnow(), new = True)
        newcmd.put()
        cmd = db.GqlQuery("SELECT * FROM CmdInfos WHERE user = :1 ORDER BY mtime",user)
        template_values = {
            'user': user,
            'cmd': cmd,
        }
        template = JINJA_ENVIRONMENT.get_template('newcmd.html')
        self.response.write(template.render(template_values))
#       	self.redirect('/newcmd')

app=webapp2.WSGIApplication([('/newcmd',MainPage)],
                            debug=True)
