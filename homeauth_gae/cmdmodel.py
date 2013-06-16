from google.appengine.ext import db
import datetime
class CmdInfos(db.Model):
    user = db.UserProperty()
    cmd = db.StringProperty()
    mtime = db.DateTimeProperty(default = datetime.datetime.utcnow())
    etime = db.DateTimeProperty(default = datetime.datetime.utcnow())
    info = db.TextProperty(default = '')
    new = db.BooleanProperty(default = False)

#    oldcmd = db.StringListProperty(default=[])
#    newcmd = db.StringListProperty(default=[])
#    client_state = db.TextProperty(default='')
#    help_msg = db.TextProperty(default='')
#    new_cmd = db.BooleanProperty(default=False)
#    last_recvcmd_time = db.DateTimeProperty(default=datetime.datetime.utcnow())
#    last_getcmd_time = db.DateTimeProperty(default=datetime.datetime.utcnow())