from google.appengine.ext import db

class PubKeys(db.Model):
    pubkey = db.TextProperty()
    user   = db.UserProperty()