from google.appengine.ext import db
import datetime
class CmdInfos(db.Model):
    user = db.UserProperty()
    oldcmd = db.StringListProperty(default=[])
    newcmd = db.StringListProperty(default=[])
    client_state = db.TextProperty(default='')
    help_msg = db.TextProperty(default='')
#    new_cmd = db.BooleanProperty(default=False)
    last_recvcmd_time = db.DateTimeProperty(default=datetime.datetime.utcnow())
    last_getcmd_time = db.DateTimeProperty(default=datetime.datetime.utcnow())