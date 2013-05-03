#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import os
import HandlePics
import CloudDir
import AudioCmd
import logging
import getopt
import Queue
log = logging.getLogger('camera')
try:
    import cv
except:
    cv = None
from settings import *
INTERVALTIME = 1
SIMILARITYLIMIT = 0.98
class Monitor(threading.Thread):
    def __init__(self):
        super(Monitor, self).__init__()
        self.close = False
        self.cam = cv.CaptureFromCAM(0)
    def run(self):
        log.info('run')
        self.takePhoto()
        time.sleep(10)
        self.close = False
        pic1 = self.takePhoto()
        CloudDir.CloudDir.wait_files.append((pic1,os.path.join(CloudDir.CloudDir.camera,os.path.basename(pic1))))
        while not self.close:
            time.sleep(INTERVALTIME)
            pic2 = self.takePhoto()
            s = self.similarity(pic1,pic2)
            log.info(s)
            if s > SIMILARITYLIMIT:#same pictures
                os.remove(pic2)
            else:
                CloudDir.CloudDir.wait_files.append((pic2,os.path.join(CloudDir.CloudDir.camera,os.path.basename(pic2))))
                pic1 = pic2
                AudioPlayer.AudioCmd.runCmd(['-p','1'])
        del(self.cam)
    def terminate(self):
        self.close = True
    def takePhoto(self):
        try:
            feed=cv.QueryFrame(self.cam)
#            cv.WaitKey(INTERVALTIME)
            cam_pic = os.path.join(CAMERA_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg')
            cv.SaveImage(cam_pic,feed)
        except Exception,data:
            log.error(data)
            return ''
        return cam_pic
    def similarity(self,pic1,pic2):
        s = HandlePics.HandlePics().similarity(pic1,pic2)
        return s
class CameraCmd(threading.Thread):
    cmdqueue = Queue.Queue()
    terminate_flag = False
    monitor = None
    def __init__(self):
        super(CameraCmd, self).__init__()
    def run(self):
        CameraCmd.terminate_flag = False
        while not CameraCmd.terminate_flag:
            cmd = CameraCmd.cmdqueue.get()
            self.runCmd(cmd)
    def runCmd(self,cmd):
        log.debug(cmd)
        optlist,args = getopt.getopt(cmd,'cs')
        for o,v in optlist:
            if o == '-c' and not CameraCmd.isCameraing():
                try:
                    CameraCmd.monitor = Monitor()
                    CameraCmd.monitor.start()
                except Exception,data:
                    log.error(data)
            if o == '-s':
                CameraCmd.terminate()
    @staticmethod
    def isCameraing():
        return CameraCmd.monitor is not None and CameraCmd.monitor.isAlive()
    @staticmethod
    def terminate():
        if CameraCmd.isCameraing():
            CameraCmd.monitor.terminate()
        CameraCmd.terminate_flag = True