# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:15:26 2023

@author: DAV1SI
"""
#This script sets the channel & trigger parameters of the oscilloscope and triggers and receives the waveform
#The data is then saved on the controlling PC and OSC with a specific trigger ID


import pandas as pd
import os
import logging
import threading
import time
import concurrent.futures

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

def SET_TRIGGER(OSC, trigger_type:str, trigger_mode:str, trigger_slope:str, trigger_coupling:str, trigger_level:float,t_div:str, v_div:float, PC_path): # OSC_path
    i = 1
    for i in range(1,5):
        
        filename = str(OSC.trig_time().replace("," , "_"))
        OSC.set_tdiv(t_div)
        OSC.set_vdiv(i, v_div)
        OSC.set_trig_source("C"+ str(i))
        OSC.set_trig_type(trigger_type)
        OSC.set_trig_coupling(("C"+ str(i)),trigger_coupling)
        OSC.set_trig_slope("C"+ str(i),trigger_slope)
        OSC.set_trig_level("C"+ str(i),trigger_level)
        OSC.set_trig_mode(trigger_mode)
        
        PC_path	= r"C:\Users\DAV1SI\Desktop\test"           #change according to your preferrred save folder on controlling PC
        
        print(f"TRIGGER ID: C{i} = {filename}")
        waveform = OSC.get_waveform(i)
        print(waveform)
            
        waveform = pd.DataFrame(waveform)
    
        OSC.save_waveform_on_OSC("Excel", i,  "C" + str(i) + "_" + filename)
        OSC.save_waveform_on_PC(PC_path, waveform,  "C" + str(i) + "_" + filename)
        OSC.save_parameters_trace(PC_path, i, 'Excel', "C" + str(i) + "_" + filename + str("_parameters_"))
        
        i +=1

    #OSC.set_trig_mode("AUTO")

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
    
    