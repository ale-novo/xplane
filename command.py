#!/usr/bin/python3

from __future__ import print_function

from time import *
from xplane import *

import json
import sys

def xp_connect():
    global xp
    xp = XPlaneUdp()

    try:
        beacon = xp.FindIp()
        print(str(sys.argv[1]))
        xp.SendCommand(sys.argv[1])

    except XPlaneIpNotFound:
      exit(1)

def xp_disconnect():
    try:
        xp
    except NameError:
        pass
    else:
        del xp

if __name__ == '__main__':

    if len(sys.argv) != 2:
      print('please type one command as argument')
      exit(1)
    xp_connect()
    xp_disconnect()
    exit(0)
