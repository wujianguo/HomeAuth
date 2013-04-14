#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import os
import HandlePics
import CloudDir
import AudioPlayer
import logging
import getopt
log = logging.getLogger('camera')
try:
    import cv
except:
    cv = None
from settings import *
INTERVALTIME = 1
SIMILARITYLIMIT = 0.91
class Monitor(threading.Thread):
    def __init__(self):
        super(Monitor, self).__init__()
        self.close = False
        self.cam = cv.CaptureFromCAM(0)
    def run(self):
        pic1 = self.takePhoto()
        CloudDir.CloudDir.saveFile(pic1,os.path.join(CloudDir.CloudDir.camera,os.path.basename(pic1)))
        while not self.close:
            time.sleep(INTERVALTIME)
            pic2 = self.takePhoto()
            s = self.similarity(pic1,pic2)
            log.info(s)
            if s > SIMILARITYLIMIT:#same pictures
                os.remove(pic2)
            else:
                CloudDir.CloudDir.saveFile(pic2,os.path.join(CloudDir.CloudDir.camera,os.path.basename(pic2)))
                pic1 = pic2
                AudioPlayer.AudioCmd.runCmd(['-p','1'])
    def terminate(self):
        self.close = True
    def takePhoto(self):
        try:
            feed=cv.QueryFrame(self.cam)
            cv.WaitKey(100)
            cam_pic = os.path.join(CAMERA_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg')
            cv.SaveImage(cam_pic,feed)
        except Exception,data:
            log.error(data)
            return ''
        return cam_pic
    def similarity(self,pic1,pic2):
        s = HandlePics.HandlePics().similarity(pic1,pic2)
        return s
class CameraCmd():
    def __init__(self):
        self.monitor = None
    def runCmd(self,cmd):
        log.debug(cmd)
        optlist,args = getopt.getopt(cmd,'cs')
        for o,v in optlist:
            if o == '-c':
                if not self.monitor or not self.monitor.isAlive():
                    try:
                        self.monitor = Monitor()
                        self.monitor.start()
                    except Exception,data:
                        log.error(data)
            if o == '-s':
                if self.monitor and self.monitor.isAlive():
                    self.monitor.terminate()
    def terminate(self):
        self.runCmd(['-s',])
