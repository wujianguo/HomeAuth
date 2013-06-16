from google.appengine.api import users
from google.appengine.ext import db
from Crypto.PublicKey import RSA
import keymodel
import os,logging

def verifyKey(enctext, encinfo):
    pri = os.path.join(os.path.dirname(__file__),'private/id_rsa')
    with open(pri) as f:
        center_privkey = f.read()
    privkey=RSA.importKey(center_privkey)
    try:
        info=privkey.decrypt(encinfo)
        gmail=info[2:int(info[0:2])+2]
        logging.info(gmail)
        msg=info[2+int(info[0:2]):]
        user=users.User(email=gmail)
        curuser=db.GqlQuery("SELECT * FROM PubKeys WHERE user = :1",user)
        userinfo=curuser.get()
    except Exception,data:
        logging.error(data)
    else:       
        if userinfo:
            pubkey=RSA.importKey(userinfo.pubkey)
            if pubkey.verify(msg,enctext):
                return user
    return None