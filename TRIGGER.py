# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:00:06 2023

@author: DAV1SI
"""

from Oscilloscope_PyVisa import Oscilloscope
from SET_TRIGGER import SET_TRIGGER
import threading
from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()


#config parameters
ip = "169.254.157.48"
channel = 1
tdiv = "20US"
vdiv = 10
trig_source = "C1"
trig_type = 'EDGE'
trig_coupling = 'DC'
trig_slope = 'Positive'
trig_mode = 'SINGLE'
trig_level = 5
pc_path = "C:\\Users\DAV1SI\Desktop\\test"
osc_path = "C:\\Users\LCRYDMIN\Desktop\\test" #there's a error in setting osc path in automation command


def create_settings_config(channel:float, trig_source:str, trig_type:str, trig_mode:str, trig_slope:str, trig_coupling:str, trig_level:float, tdiv:str, vdiv:float, pc_path:str):  # include OSC_path later
    #Create config files for Channel, Trigger and Save settings
    config_object["Channel Settings"] = {
        "channel": channel,
        "tdiv": tdiv,
        "vdiv": vdiv
    }

    config_object["Trigger Settings"] = {
        "trigger source": trig_source,
        "trigger type": trig_type,
        "trigger coupling": trig_coupling,
        "trigger slope" : trig_slope,
        "trigger mode" : trig_mode, 
        "trigger level" : trig_level
    }

    config_object["Save Paths"] = {
        "PC path": pc_path,
        "OSC path": osc_path
    }

    #Write the above sections to config.ini file
    with open(f'ch_{channel}_config.ini', 'w') as conf:
        config_object.write(conf)


# create_settings_config(2, "C2", "EDGE", "SINGLE", "Negative", "DC", 10, "10US", 20, "C:\\Users\DAV1SI\Desktop\test")
# create_settings_config(3, "C3", "EDGE", "SINGLE", "Negative", "DC", 5, "10US", 50, "C:\\Users\DAV1SI\Desktop\test")
# create_settings_config(4, "C4", "EDGE", "SINGLE", "Positive", "DC", 0, "10US", 70, "C:\\Users\DAV1SI\Desktop\test")

def read_settings_config(channel:float):
    config_object.read(f"ch_{channel}_config.ini")

    channel_settings = config_object["Channel Settings"]
    ch = channel_settings["channel"]
    tdiv = channel_settings["tdiv"]
    vdiv = channel_settings["vdiv"]

    trigger_settings = config_object["Trigger Settings"]
    trigger_source = trigger_settings["trigger source"]
    trigger_type = trigger_settings["trigger type"]
    trigger_coupling = trigger_settings["trigger coupling"]
    trigger_slope = trigger_settings["trigger slope"]
    trigger_mode = trigger_settings["trigger mode"]
    trigger_level = trigger_settings["trigger level"]

    path__settings = config_object["Save Paths"]
    PC_path = path__settings["PC path"]
    OSC_path = path__settings["OSC path"]
    	
    return ch, tdiv, vdiv, trigger_source, trigger_type, trigger_coupling, trigger_level, trigger_slope, trigger_mode, trigger_level, PC_path, OSC_path


if __name__ == "__main__":
    osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")

    # id = SET_TRIGGER(osc, trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path)  # There's some error with osc_path
    # print(f"\nTrigger ID =  {id}")


    t1 = threading.Thread(target= SET_TRIGGER(osc, channel, trig_source, trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path))
    t2 = threading.Thread(target= SET_TRIGGER(osc, 2, "C2", trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path))
    t3 = threading.Thread(target=SET_TRIGGER(osc, 3, "C3", trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path))
    t4 = threading.Thread(target=SET_TRIGGER(osc, 4, "C4", trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()