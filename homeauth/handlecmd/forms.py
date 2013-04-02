from django import forms
from userena.utils import user_model_label
from django.contrib.auth.models import User
from verify.models import VerifyUsers
from homeauth.settings import *
from Crypto.PublicKey import RSA
import logging
#logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')
class CmdForm(forms.Form):
    camera_cmd = forms.CharField(widget=forms.Textarea)
    screen_cmd = forms.CharField(widget=forms.Textarea)
    audio_out_cmd  = forms.CharField(widget=forms.Textarea)
class VerifyForm(forms.Form):
    signature = forms.CharField(widget=forms.Textarea)
    userinfo  = forms.CharField(widget=forms.Textarea)
#    encrpymsg = forms.CharField(widget=forms.Textarea)
    def getUser(self):
        enc = self.cleaned_data['userinfo']
        sig = self.cleaned_data['signature']
        try:
            enctext=eval(enc)
            encsig=eval(sig)
        except Exception,data:
            logging.error(data)
            return None
        with open(PRIVATE_KEY_PATH) as f:
            center_privkey = f.read()
        try:
            center_privkey=RSA.importKey(center_privkey)
            info = center_privkey.decrypt(enctext)
        except Exception,data:
            logging.error(data)
            return None
        user_email,user_signature = self.getEmail(info)
        try:
            user = User.objects.get(email = user_email)
            userkey = VerifyUsers.objects.get(user = user)
        except User.DoesNotExist:
            return None
        except VerifyUsers.DoesNotExist:
            return None
        if not userkey.pubkey:
            return None
        try:
            pubkey = RSA.importKey(userkey.pubkey)
        except Exception,data:
            logging.error(data)
            return None
        if not pubkey.verify(user_signature,encsig):
            return None
        return user
    
    def getEmail(self,s):
        import string
        if len(s)<=2 or s[0] not in string.digits or s[1] not in string.digits:
            return '',''
        l = int(s[:2])
        if len(s)<2+l:
            return '',''
        return s[2:l+2],s[l+2:]
