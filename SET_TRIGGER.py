# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:15:26 2023

@author: DAV1SI
"""
#This script sets the channel & trigger parameters of the oscilloscope and triggers and receives the waveform
#The data is then saved on the controlling PC and OSC with a specific trigger ID


import pandas as pd
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

def SET_TRIGGER(OSC, channel:float, trig_source:str, trigger_type:str, trigger_mode:str, trigger_slope:str, trigger_coupling:str, trigger_level:float,t_div:str, v_div:float, PC_path:str): # OSC_path
        
        filename = str(OSC.trig_time().replace("," , "_"))
        OSC.set_tdiv(t_div)
        OSC.set_vdiv(channel, v_div)
        OSC.set_trig_source("C"+ str(channel))
        OSC.set_trig_type(trigger_type)
        OSC.set_trig_coupling(trig_source,trigger_coupling)
        OSC.set_trig_slope(trig_source,trigger_slope)
        OSC.set_trig_level(trig_source,trigger_level)
        OSC.set_trig_mode(trigger_mode)
        
        PC_path	= r"C:\Users\DAV1SI\Desktop\test"           #change according to your preferrred save folder on controlling PC
        
        print(f"TRIGGER ID: C{channel} = {filename}")
        waveform = OSC.get_waveform(channel)
        print(waveform)
            
        waveform = pd.DataFrame(waveform)

        OSC.save_waveform_on_OSC("Excel", channel,  "C" + str(channel) + "_" + filename)
        OSC.save_waveform_on_PC(PC_path, waveform,  "C" + str(channel) + "_" + filename)
        OSC.save_parameters_trace(PC_path, channel, 'Excel', "C" + str(channel) + "_" + filename + str("_parameters_"))
        
    

        OSC.set_trig_mode("AUTO")

# def GET_WAVEFORM_FROM_PC(OSC, ID:str):    #WORK IN PROGRESS
#     pc_path = r"C:\Users\DAV1SI\Desktop\test"
#     file_path = os.path.join(pc_path, ID)
    
#     # Check if the file exists
#     if os.path.exists(file_path):
#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(file_path)
#         return df
#     else:
#         print(f"The file {ID} does not exist in the specified folder.")
        
#         return None
#     OSC.write("""vbs 'app.SaveRecall.Waveform.WaveformDir = "C:\\Users\\LCRYDMIN\\Desktop\\test" '""") #copy from a specific folder
#     OSC.write(f"vbs 'app.SaveRecall.Waveform.RecallFilename = \"{ID}\"'") #copy a specific curve

#     #self.write("vbs' app.SaveRecall.Utilities.DestDirectory'")
#    #file_path = r"C:\Users\DAV1SI\Desktop\test"
#    #os.path.join(osc_path, id)
#     print("FIle saved successfuly on PC")
    
    