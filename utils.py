import threading
from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

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
        "OSC path": "C:\\Users\LCRYDMIN\Desktop\\test"
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