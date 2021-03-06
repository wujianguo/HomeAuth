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
    terminate_flag = False
    def __init__(self):
        super(CodeCmd, self).__init__()
    def run(self):
        CodeCmd.terminate_flag = False
        while not CodeCmd.terminate_flag:
            try:
                cmd = CodeCmd.cmdqueue.get(True, 0.1)
            except Queue.Empty:
                pass
            else:
                self.runCmd(cmd)
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
    def terminate():
        CodeCmd.terminate_flag = True
