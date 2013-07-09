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
    close_event = threading.Event()
    terminate_event = threading.Event()
    def __init__(self):
        super(ScreenCmd, self).__init__()
    def run(self):
        while not ScreenCmd.terminate_event.isSet():
            try:
                cmd = ScreenCmd.cmdqueue.get(True, 0.1)
            except Queue.Empty:
                if ScreenCmd.close_event.isSet():
                    break
            else:
                try:
                    self.runCmd(cmd)
                except Exception as e:
                    log.error(e)
    def runCmd(self,cmd):
        p = self.takeAShot()
        if p:
            CloudDir.CloudDir.wait_files.append((p,os.path.join(CloudDir.CloudDir.screen,os.path.basename(p))))
    @staticmethod
    def addTask(cmd):
        ScreenCmd.cmdqueue.put(cmd)
    def takeAShot(self):
        if grab:
            img = grab()
            img_path = os.path.join(SCREEN_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.jpg')
            img.save(img_path)
            return img_path
        return ''
    def close(self):
        ScreenCmd.close_event.set()
    def terminate(self):
        ScreenCmd.terminate_event.set()