import webapp2

from google.appengine.api import users
import jinja2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        template_values = {
            'user': user,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)