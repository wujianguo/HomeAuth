#! /usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import logging
log = logging.getLogger('screen')
try:
    from ImageGrab import grab
except:
    grab = None
from settings import *
import CloudDir
class ScreenCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        p = self.takeAShot()
        if p:
            CloudDir.CloudDir.saveFile(p,os.path.join(CloudDir.CloudDir.screen,os.path.basename(p)))
    def takeAShot(self):
        if grab:
            img = grab()
            img_path = os.path.join(SCREEN_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg')
            img.save(img_path)
            return img_path
        return ''