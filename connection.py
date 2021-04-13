#!/usr/bin/python3

from __future__ import print_function
from time import *

from xplane import *
from utils import *

import sys
import os
import datetime


class xplane_connection:
    def __init__(self, datarefs, rate):
        self.xp = None
        self.datarefs = datarefs
        self.rate = rate

    def xp_connect(self):
        self.xp = XPlaneUdp()
        self.xp.defaultFreq = self.rate
        try:
            beacon = self.xp.FindIp()
            print('Loading ' + str(len(self.datarefs)) + ' Datarefs')
            for value in self.datarefs:
                self.xp.AddDataRef(value)

        except XPlaneIpNotFound:
            print("X-Plane not found")

    def xp_disconnect(self):
        try:
            self.xp
        except NameError:
            pass
        else:
            del self.xp

    #@timeit
    def get_dataref(self):
        try:
            values = self.xp.GetValues()

            while len(values) != len(self.datarefs):
                difference=list(self.datarefs - values.keys())
                for item in difference:
                    self.xp.AddDataRef(item)
                values = self.xp.GetValues()

        except XPlaneTimeout:
            print("X-Plane timeout, reconecting...")
            self.xp_disconnect()
            sleep(2.0)
            self.xp_connect()
            values = None

        return values

    def send_command(self, command):
        if command is not None:
            self.xp.SendCommand(command)

    def write_dataref(self, dataref, value, vtype='float'):
        if dataref is not None and value is not None:
            self.xp.WriteDataRef(dataref, value, vtype)

