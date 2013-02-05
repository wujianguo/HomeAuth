#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,os.path,logging,logging.handlers

def init_log():
    py_path=os.path.realpath(__file__)
    log_path=os.path.join(os.path.split(py_path)[0],"log")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_name=os.path.basename(py_path)[0:os.path.basename(py_path).rfind('.')]+".log"
    log_file=os.path.join(log_path,log_name)
    logformat='[%(levelname)s %(asctime)s %(filename)s \
%(module)s %(funcName)s line:%(lineno)d] %(message)s'
    console = logging.StreamHandler()
    stdlog=logging.getLogger("stdlog")
    stdlog.addHandler(console)
    console = logging.handlers.RotatingFileHandler(filename=log_file,
                                                    mode='a',
                                                    maxBytes=20*1024*1024,
                                                    backupCount=20)
    console.setFormatter(logging.Formatter(logformat))
    stdlog.addHandler(console)
    stdlog.setLevel(logging.DEBUG)
init_log()
stdlog=logging.getLogger("stdlog")

from dropbox import client,rest,session
from datetime import datetime
import webbrowser,sys,time,tempfile
APP_KEY='d6f5yzu2f45eydr'
APP_SECRET='ah3uohrf90ls6a7'
ACCESS_TYPE='app_folder'


import cv

def cams():
    cv.NamedWindow("webcam",cv.CV_WINDOW_AUTOSIZE)
    cam=cv.CaptureFromCAM(-1)
    for i in range(10):
        feed=cv.QueryFrame(cam)
        cv.ShowImage("webcam",feed)
        cv.WaitKey(100)
        cv.SaveImage(str(i)+".jpg",feed)
        
def createfolder(cl,path):
    try:
        cl.file_create_folder(path)
    except rest.ErrorResponse,d:
        stdlog.debug(d)
def quotapercent(cl):
    infos=cl.account_info()
    usedbytes=infos['quota_info']['shared']+infos['quota_info']['normal']
    quota=infos['quota_info']['quota']
    return 1.0*usedbytes/quota
def uploadnewfile(dropboxpath,cl):
    while True:
        nowtime=datetime.now().strftime("%Y%m%d%H%M%S")
        qc=quotapercent(cl)
        stdlog.debug('%s %d %f'%(nowtime,i,quotapercent(cl)))
        if qc>0.8:
            break
        f=tempfile.TemporaryFile()
        f.write(nowtime)
        f.seek(0)
        cl.put_file(os.path.join(dropboxpath,nowtime+'.txt'),f)
        f.close()
        time.sleep(1)
def main():
    if len(sys.argv)!=2:
        return
    file_path=sys.argv[1]
    sess=session.DropboxSession(APP_KEY,APP_SECRET,ACCESS_TYPE)
    request_token=sess.obtain_request_token()
    url=sess.build_authorize_url(request_token)
    print("url:"+url)
    webbrowser.open(url)
    raw_input()
    access_token=sess.obtain_access_token(request_token)
    cl=client.DropboxClient(sess)
    
    dropboxpath='/screens'
    createfolder(cl,dropboxpath)
    uploadnewfile(dropboxpath,cl)
if __name__=='__main__':
    main()