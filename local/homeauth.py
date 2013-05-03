#! /usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '2.0.0'
import logging
import Queue
import os
import time
import requests,urllib
from Crypto.PublicKey import RSA
import Crypto.Random
from settings import *
import CameraCmd
import ScreenCmd
import AudioCmd
import SystemCmd
import CodeCmd
import CloudDir
class HomeAuth():
    def __init__(self,key_path,email):
        self.key_path = key_path
        self.email = email
        self.pub = ''
        self.log = logging.getLogger('cmd')
        self.cmdpro = {
            'system':SystemCmd.SystemCmd,
            'camera':CameraCmd.CameraCmd,
            'screen':ScreenCmd.ScreenCmd,
            'audio':AudioCmd.AudioCmd,
            'code':CodeCmd.CodeCmd,
            'clouddir':CloudDir.CloudDir,
        }
        for pro in self.cmdpro:
            self.cmdpro[pro]().start()
    def getCmd(self):      
        if not self.pub:
            f = requests.get(ID_RSA_PUB,proxies=PROXY)
            self.pub = f.text
        pubkey = RSA.importKey(self.pub)
        with open(self.key_path) as f:
            privkey = RSA.importKey(f.read())
        sig = Crypto.Random.new().read(16)
        info = str(len(self.email))+self.email+sig
        if len(self.email) < 10:
            info = '0' + info
        signature = privkey.sign(sig,'')
        encinfo = pubkey.encrypt(info,32)
        para=({'signature':repr(signature),'userinfo':repr(encinfo)})
        urllib.urlencode(para)
        r = requests.post(GET_CMD_URL,data=para,proxies=PROXY,timeout=TIME_OUT)
        self.log.debug(r.json())
        return r.json()
    def handleCmd(self):
        t = REQUESTS_TIME.total_seconds()
        self.log.debug(t)
        while True:
            try:
                cmd = self.getCmd()
            except Exception,data:
                self.log.error(data)
                t = REQUESTS_TIME.total_seconds() + t
            else:
                if cmd['err'] == 'ok':
                    self.log.info(cmd['response']['newcmd'])
                    for c in cmd['response']['newcmd']:
                        cmdline = c.strip().split()
                        if len(cmdline)<=1:
                            continue
                        try:
                            self.cmdpro[cmdline[0]].cmdqueue.put(cmdline[1:])
                        except Exception,data:
                            self.log.error(data)
                t = REQUESTS_TIME.total_seconds()
            finally:
                try:
                    time.sleep(t)
                except:
                    for i in self.cmdpro:
                        self.cmdpro[i].terminate()
                    break
def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    h = HomeAuth(USER_PRIVKEY_PATH, USER_EMAIL.strip())
    h.handleCmd()
if __name__=='__main__':
    main()
