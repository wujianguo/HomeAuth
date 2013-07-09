#!/usr/bin/env python
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
        ScreenCmd.terminate_flag = False
        while not ScreenCmd.terminate_flag:
            try:
                cmd = ScreenCmd.cmdqueue.get(True, 0.1)
            except Queue.Empty:
                pass
            else:
                self.runCmd(cmd)
    def runCmd(self,cmd):
        p = self.takeAShot()
        if p:
            CloudDir.CloudDir.wait_files.append((p,os.path.join(CloudDir.CloudDir.screen,os.path.basename(p))))
    def takeAShot(self):
        if grab:
            img = grab()
            img_path = os.path.join(SCREEN_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg')
            img.save(img_path)
            return img_path
        return ''
    @staticmethod
    def terminate():
        ScreenCmd.terminate_flag = True