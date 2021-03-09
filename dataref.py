#!/usr/bin/python3

from __future__ import print_function

from time import *
from xplane import *

import json
import sys

datarefs = sys.argv[1:]

def xp_connect():
    global xp
    xp = XPlaneUdp()

    try:
        beacon = xp.FindIp()
        for value in datarefs:
            xp.AddDataRef(value)

    except XPlaneIpNotFound:
      exit(1)

def xp_disconnect():
    try:
        xp
    except NameError:
        pass
    else:
        del xp

def get_dataref():
    try:
        values = xp.GetValues()
        while len(values) != len(datarefs):
            difference=list(datarefs-values.keys())
            for item in difference:
                xp.AddDataRef(item)
            values = xp.GetValues()

    except XPlaneTimeout:
        xp_disconnect()
        values = None
        code = 1

    return values

if __name__ == '__main__':
    if len(datarefs) == 0:
      print('please type at least one dataref as argument')
      exit(1)
    xp_connect()

data = get_dataref()
if data is not None:
   print(json.dumps(data))
   code = 0
xp_disconnect()
exit(code)
