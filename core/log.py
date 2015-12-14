# -*- coding: utf-8 -*-

import time

logfilename = None

def log(s):
    global logfilename
    if not logfilename:
        logfilename = time.time()
    logfile = open("log\\log_{}.log".format(logfilename), "a")
    logfile.write(s+"\n")
    logfile.close()