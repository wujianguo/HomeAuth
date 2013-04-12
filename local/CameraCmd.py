#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import os
import HandlePics
import CloudDir
import AudioPlayer
#from settings import *
INTERVALTIME = 1
SIMILARITYLIMIT = 0.8
class Monitor(threading.Thread):
    def __init__(self):
        super(Monitor, self).__init__()
        self.close = False
    def run(self):
        pic1 = self.takePhoto()
        while not self.close:
            time.sleep(INTERVALTIME)
            pic2 = self.takePhoto()
            s = self.similarity(pic1,pic2)
            if s > SIMILARITYLIMIT:#same pictures
                os.remove(pic2)
            else:
                CloudDir.CloudDir.saveFile(p,os.path.join(CloudDir.CloudDir.camera,os.path.basename(pic2)))
                pic1 = pic2
                AudioPlayer.AudioCmd.runCmd('-p 1')
    def terminate(self):
        self.close = True
    def takePhoto(self):
        return ''
    def similarity(self,pic1,pic2):
        s = HandlePics.HandlePics().similarity(pic1,pic2)
        return s
class CameraCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        pass
