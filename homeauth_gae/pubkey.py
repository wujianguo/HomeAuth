import webapp2
import keymodel
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
            'key':'',
        }

        curuser=db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1",user)
        userinfo=curuser.get()
        if userinfo:
        	template_values.update({'key':userinfo})
       	else:
			newuser=keymodel.PubKeys(user=user,pubkey='')
			newuser.put()
        template = JINJA_ENVIRONMENT.get_template('pubkey.html')
        self.response.write(template.render(template_values))
    def post(self):
    	user = users.get_current_user()
    	curuser=db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1",user)
        userinfo=curuser.get()
        if userinfo:
            userinfo.pubkey=self.request.get('pubkey')
            userinfo.put()
       	else:
            newuser=keymodel.PubKeys(user=user,pubkey=self.request.get('pubkey'))
            newuser.put()
       	self.redirect('/pubkey')

app=webapp2.WSGIApplication([('/pubkey',MainPage)],
                            debug=True)
