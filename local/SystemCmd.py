#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
class SystemCmd():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        os.system(' '.join(cmd))
    def terminate(self):
        pass
