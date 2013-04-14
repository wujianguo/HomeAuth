#! /usr/bin/env python
# -*- coding: utf-8 -*-
from dropbox import client,rest,session
from datetime import datetime
import webbrowser,sys,time,tempfile,logging,os
import getopt,random,string
from settings import *
stdlog = logging.getLogger('clouddir')
import MySmtp
class CloudDir():
    sess = None
    cl = None
    request_token = None
    id = ''
    screen = '/screen'
    camera = '/camera'
    def __init__(self):
        pass
    def reset(self):
        CloudDir.sess = None
        CloudDir.cl = None
        CloudDir.request_token = None
        CloudDir.id = ''
    def runCmd(self,cmd):
        optlist,args = getopt.getopt(cmd,'i:s')
        for o,v in optlist:
            if o=='-i':
                self.notify_authorize(v)
            if o=='-s':
                self.authorize()
    @staticmethod
    def saveFile(localfile,cloudfile):
        cloudfile = cloudfile.replace('\\','/')
        stdlog.debug(localfile)
        stdlog.debug(cloudfile)
        if not CloudDir.cl:
            stdlog.debug('not open clouddir')
            return
        stdlog.debug('start upload')
        with open(localfile,'rb') as f:
            CloudDir.cl.put_file(cloudfile,f)
    def createDirs(self,dirs):
        m = CloudDir.cl.metadata('/')
        exist_dirs = []
        for i in m['contents']:
            if i['is_dir']:
                exist_dirs.append(i['path'])
        for d in dirs:
            if d not in exist_dirs:
                try:
                    CloudDir.cl.file_create_folder(d)
                except rest.ErrorResponse,data:
                    stdlog.error(data)
    def authorize(self):
        try:
            CloudDir.sess=session.DropboxSession(APP_KEY,APP_SECRET,ACCESS_TYPE)
            CloudDir.request_token=CloudDir.sess.obtain_request_token()
            url=CloudDir.sess.build_authorize_url(CloudDir.request_token)
        except Exception, data:
            stdlog.error(data)
            self.reset()
            return False
        stdlog.info("url:"+url)
        CloudDir.id = ''.join(random.sample(string.ascii_letters,4))
        if self.send_mail('dropbox','clouddir -i '+CloudDir.id+' url:'+url):
            stdlog.debug('send_mail ok')
            return True
        else:
            self.reset()
            return False        
    def notify_authorize(self,id):
        if id == CloudDir.id:
            try:
                access_token=CloudDir.sess.obtain_access_token(CloudDir.request_token)
                CloudDir.cl=client.DropboxClient(CloudDir.sess)
                self.createDirs([self.screen,self.camera])
            except Exception,data:
                stdlog.error(data)
                self.reset()
    def send_mail(self,subject,msg_content):
        m = MySmtp.EmailBackend(EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)
        return m.send_messages(RECV_MSG_EMAIL, subject, msg_content)
    def quotapercent(self):
        infos = CloudDir.cl.account_info()
        usedbytes = infos['quota_info']['shared']+infos['quota_info']['normal']
        quota = infos['quota_info']['quota']
        return 1.0*usedbytes/quota
    @staticmethod
    def terminate():
        pass
        
