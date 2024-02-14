# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:00:06 2023

@author: DAV1SI
"""
import time
from Oscilloscope_PyVisa import Oscilloscope
from SET_TRIGGER_SEQ import SET_SINGLE_TRIGGER, SET_NORMAL_TRIGGER

'''CONFIG PARAMETERS'''

#osc IP
ip = "192.168.240.50"

#timebase or horizontal settings
sampling_mode = "RealTime"
tdiv = "20MS"
sample_rate = "SetMaximumMemory"
max_sample_points = 1e+6
num_active_channels = "8"

#channel vertical settings
vdiv = 10
ver_offset = 1.2
units_per_volt = 10.0
variable_gain_status = True
channel_coupling = "DC50"

#save/recall setup
setup_filename = "setup_vedant_12.02.24.lss"

#trigger settings
trig_source = "C6"
trig_type = 'EDGE'
trig_coupling = 'DC'
trig_slope = 'Negative'
trig_mode = 'SINGLE'
trig_level = 1.2
trig_delay = -20e-3

#data retrival settings
source_folder = r"C:\Users\DAV1SI\Desktop\test"
target_folder = r"C:\Users\DAV1SI\Desktop\Waveforms"
id = r"C2_12_FEB_2024"

if __name__ == "__main__":

    #connection to Oscilloscope
    osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")

    #setting TImebase settings for ALL channels
    osc.timebase_settings(sampling_mode,tdiv,sample_rate,max_sample_points,num_active_channels) #issues with 10.0MS, 10MS, 2.500000000 GS/s
    
    #setting individual channel parameters
    osc.SET_CHANNEL_PARAMETERS(6, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 1   
    osc.SET_CHANNEL_PARAMETERS(7, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 2
    # osc.SET_CHANNEL_PARAMETERS(3, '5MS',2)  #channel 3
    # osc.SET_CHANNEL_PARAMETERS(4, '5MS',1)  #channel 4
    # osc.SET_CHANNEL_PARAMETERS(5, '5MS',6)  #channel 5
    # osc.SET_CHANNEL_PARAMETERS(6, '5MS',2)  #channel 6
    # osc.SET_CHANNEL_PARAMETERS(7, '5MS',8)  #channel 7
    # osc.SET_CHANNEL_PARAMETERS(8, '5MS',9)  #channel 8

    #save setup file on OSC
    # osc.save_setup('File',False, fr'C:\Users\LCRYDMIN\Setups\{setup_filename}') 
    # print("Setup Saved")

    # print(".....")
    # time.sleep(5)

    # # recall prior saved custom setup from OSCs
    # osc.recall_setup('File', fr'C:\Users\LCRYDMIN\Setups\{setup_filename}') 
    # print("Recall Setup Successfull!")

    # #SINGLE triggering the signal
    # start_time = time.time()
    # id1 = SET_SINGLE_TRIGGER(osc, trig_source, trig_type, trig_slope, trig_coupling, trig_level, trig_delay, max_sample_points)
    # print("--- %s seconds ---" % round(time.time() - start_time, 3))
    # print(id1)

    # #saving data with specific trigger ID in folder with name as same trigger ID
    # osc.retrieve_waveform_PC(source_folder, target_folder, id1)
    

    #NORMAL triggering the signal
    start_time = time.time()
    id2 = SET_NORMAL_TRIGGER(osc, trig_source, trig_level, max_sample_points)
    print("--- %s seconds ---" % round(time.time() - start_time, 3))
    print(id2)

    #saving data with specific trigger ID in folder with name as same trigger ID
    osc.retrieve_waveform_PC(source_folder, target_folder, id2)
    