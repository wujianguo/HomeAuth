#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt,threading,Queue
import subprocess
import requests
import logging
from settings import *
log = logging.getLogger('code')
class CodeCmd(threading.Thread):
    cmdqueue = Queue.Queue()
    # music_player = None
    close_event = threading.Event()
    terminate_event = threading.Event()
    def __init__(self):
        super(CodeCmd, self).__init__()
    def run(self):
        while not CodeCmd.terminate_event.isSet():
            try:
                cmd = CodeCmd.cmdqueue.get(True, 0.1)
            except Queue.Empty:
                if CodeCmd.close_event.isSet():
                    break
            else:
                try:
                    self.runCmd(cmd)
                except Exception as e:
                    log.error(e)
    def runCmd(self,cmd):
        logging.debug(cmd)
        optlist,args = getopt.getopt(cmd,'u:')
        for o,v in optlist:
            if o == '-u':
                r = requests.get(v,proxies=PROXY)
                p = os.path.join(CODE_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.py')
                with open(p,'w') as f:
                    f.write(r.text)
                cmd = ['python',p]
                pro = subprocess.Popen(cmd)
    @staticmethod
    def addTask(cmd):
        CodeCmd.cmdqueue.put(cmd)
    def close(self):
        CodeCmd.close_event.set()
    def terminate(self):
        CodeCmd.terminate_event.set()
