# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:00:06 2023

@author: DAV1SI
"""

from Oscilloscope_PyVisa import Oscilloscope
from SET_TRIGGER import SET_TRIGGER



#config parameters
ip = "192.168.40.26"
#channel = 1
tdiv = "20US"
vdiv = 10
#trig_source = "C1"
trig_type = 'EDGE'
trig_coupling = 'DC'
trig_slope = 'Positive'
trig_mode = 'SINGLE'
trig_level = 5
pc_path = "C:\\Users\DAV1SI\Desktop\test"
osc_path = "C:\\Users\LCRYDMIN\Desktop\test" #there's a error. will debug it next week


osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")

id = SET_TRIGGER(osc, trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path)  # There's some error with osc_path
print(f"\nTrigger ID =  {id}")
