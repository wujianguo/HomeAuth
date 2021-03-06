#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,threading,Queue
class SystemCmd(threading.Thread):
    cmdqueue = Queue.Queue()
    terminate_flag = False
    def __init__(self):
        super(SystemCmd, self).__init__()
    def run(self):
    	SystemCmd.terminate_flag = False
    	while not SystemCmd.terminate_flag:
            try:
        		cmd = SystemCmd.cmdqueue.get(True, 0.1)
            except Queue.Empty:
                pass
            else:
        		self.runCmd(cmd)
    def runCmd(self,cmd):
        os.system(' '.join(cmd))
    @staticmethod
    def terminate():
        SystemCmd.terminate_flag = True
