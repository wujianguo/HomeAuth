#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,threading,Queue,logging
log = logging.getLogger('system')
class SystemCmd(threading.Thread):
    cmdqueue = Queue.Queue()
    close_event = threading.Event()
    terminate_event = threading.Event()
    def __init__(self):
        super(SystemCmd, self).__init__()
    def run(self):
    	while not SystemCmd.terminate_event.isSet():
            try:
                cmd = SystemCmd.cmdqueue.get(True, 0.1)
            except Queue.Empty:
                if SystemCmd.close_event.isSet():
                    break
            else:
                try:
                    self.runCmd(cmd)
                except Exception as e:
                    log.error(e)
    def runCmd(self,cmd):
        os.system(' '.join(cmd))
    @staticmethod
    def addTask(cmd):
        SystemCmd.cmdqueue.put(cmd)
    def close(self):
        SystemCmd.close_event.set()
    def terminate(self):
        SystemCmd.terminate_event.set()
