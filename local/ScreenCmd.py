#! /usr/bin/env python
# -*- coding: utf-8 -*-

import getopt,Queue,threading
import logging
log = logging.getLogger('screen')
try:
    from ImageGrab import grab
except:
    grab = None
from settings import *
import CloudDir
class ScreenCmd(threading.Thread):
    cmdqueue = Queue.Queue()
    terminate_flag = False
    def __init__(self):
        super(ScreenCmd, self).__init__()
    def run(self):
        while not terminate_flag:
            cmd = ScreenCmd.cmdqueue.get()
            self.runCmd(cmd)
    def runCmd(self,cmd):
        p = self.takeAShot()
        if p:
            CloudDir.CloudDir.wait_files.append((p,os.path.join(CloudDir.CloudDir.screen,os.path.basename(p))))
            CloudDir.CloudDir.cmdqueue.put('-f')
    def takeAShot(self):
        if grab:
            img = grab()
            img_path = os.path.join(SCREEN_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg')
            img.save(img_path)
            return img_path
        return ''
    def terminate(self):
        terminate_flag = True