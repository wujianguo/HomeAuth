#! /usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import subprocess
import requests
import logging
from settings import *
log = logging.getLogger('code')
class CodeCmd():
    def __init__(self):
        pass
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
    def terminate(self):
        pass
