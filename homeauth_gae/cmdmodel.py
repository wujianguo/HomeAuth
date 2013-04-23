from google.appengine.ext import db

class PubKeys(db.Model):
    user = db.UserProperty()
    cmdline = db.StringListProperty()
    client_state = db.TextProperty()
    help_msg = db.TextProperty()
    new_cmd = db.BooleanProperty(default=False)
    last_recvcmd_time = db.DateTimeProperty()
    last_getcmd_time = db.DateTimeProperty()