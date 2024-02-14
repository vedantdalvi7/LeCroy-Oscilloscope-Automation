# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:00:06 2023

@author: DAV1SI
TRIGGER_SEQ.py has all the configurable Channel, Timebase and Trigger parameters to trigger the OSC in SINGLE or NORMAL mode 
and save the triggered waveforms & it's parameters on the controlling PC.
"""
import time
from Oscilloscope_PyVisa import Oscilloscope
from SET_TRIGGER_SEQ import SET_SINGLE_TRIGGER, SET_NORMAL_TRIGGER

'''CONFIG PARAMETERS'''

#osc IP
ip = "192.168.240.50"

#turn ON/OFF Channel Trace as per requirement
trace_status = {'C1':'OFF','C2':'OFF','C3':'OFF','C4':'OFF','C5':'OFF','C6':'ON','C7':'ON','C8':'OFF'}

#timebase or horizontal settings
sampling_mode = "RealTime"         #['RealTime', 'Sequence']
tdiv = "2MS"                       #{'1NS','2NS','5NS','10NS','20NS','50NS','100NS','200NS','500NS','1US','2US','5US','10US','20US','50US','100US','200US','500US','1MS','2MS','5MS','10MS','20MS','50MS','100MS','200MS','500MS','1S','2S','5S','10S','20S','50S','100S'}
sample_rate = "SetMaximumMemory"   #['SetMaximumMemory', 'FixedSampleRate']
max_sample_points = 1e+6           #float value from 500 to 250e+6
num_active_channels = "8"          #["8","4","2","Auto"]

#channel vertical settings
vdiv = 10                        #float value between 10.0V and 10e-3V
ver_offset = 0.0                 #float value between 100V and -100V
units_per_volt = 10.0            #float value between 1.0 and -1.0
variable_gain_status = True      #bool value True or False
channel_coupling = "DC50"        #['DC50', 'Gnd', 'DC1M', 'AC1M']

#save/recall setup
setup_filename = "setup_vedant_14.02.24.lss"

#trigger settings
trig_source = "C7"               #{'C1','C2','C3','C4', 'C5', 'C6', 'C7', 'C8', 'Ext','Line','FastEdge'}
trig_type = 'EDGE'               #{'EDGE', 'WIDTH', 'PATTERN', 'SMART', 'MEASUREMENT' , 'TV', 'MULTISTAGE'}
trig_coupling = 'DC'             #{'AC','DC','HFREJ','LFREJ'}
trig_slope = 'Negative'          #{'Positive', 'Negative', 'Either'}
trig_mode = 'SINGLE'             #SINGLE, NORMAL
trig_level = 10.0                #float value between -41.0V to 41.0V
trig_delay = 0.0                 #float value between -20.0s to 20.0s

#data retrival settings
source_folder = r"C:\Users\DAV1SI\Desktop\test"
target_folder = r"C:\Users\DAV1SI\Desktop\Waveforms"
id = r"C2_12_FEB_2024"

if __name__ == "__main__":

    #connect to Oscilloscope
    osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")

    #set channel traces ON/OFF
    for source, status in trace_status.items():
        osc.set_trace(source,status)

    #setting Timebase settings for ALL channels
    osc.timebase_settings(sampling_mode,tdiv,sample_rate,max_sample_points,num_active_channels) #issues with 10.0MS, 10MS, 2.500000000 GS/s
    
    #setting individual channel parameters
    osc.SET_CHANNEL_PARAMETERS(1, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 1   
    osc.SET_CHANNEL_PARAMETERS(2, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 2
    osc.SET_CHANNEL_PARAMETERS(3, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 3   
    osc.SET_CHANNEL_PARAMETERS(4, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 4
    osc.SET_CHANNEL_PARAMETERS(5, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 5   
    osc.SET_CHANNEL_PARAMETERS(6, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 6
    osc.SET_CHANNEL_PARAMETERS(7, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 7   
    osc.SET_CHANNEL_PARAMETERS(8, vdiv, ver_offset, units_per_volt, variable_gain_status, channel_coupling)  #channel 8

    #save setup file on OSC
    # osc.save_setup('File',False, fr'C:\Users\LCRYDMIN\Setups\{setup_filename}') 
    # print("Setup Saved")
    # print(".....")
    # time.sleep(5)

    # # recall prior saved custom setup from OSCs
    # osc.recall_setup('File', fr'C:\Users\LCRYDMIN\Setups\{setup_filename}') 
    # print("Recall Setup Successfull!")

    if trig_mode == "SINGLE":
        #SINGLE triggering the signal
        start_time = time.time()
        id1 = SET_SINGLE_TRIGGER(osc, trace_status, trig_source, trig_slope, trig_coupling, trig_level, trig_delay, max_sample_points)
        print("--- %s seconds ---" % round(time.time() - start_time, 3))
        print(id1)

        #saving data with specific trigger ID in folder with name as same trigger ID
        osc.retrieve_waveform_PC(source_folder, target_folder, id1)
        

    elif trig_mode == "NORMAL":
        #NORMAL triggering the signal
        start_time = time.time()
        id1 = SET_NORMAL_TRIGGER(osc, trace_status, trig_source, trig_slope, trig_coupling, trig_level, trig_delay, max_sample_points)
        print("--- %s seconds ---" % round(time.time() - start_time, 3))
        print(id1)

        #saving data with specific trigger ID in folder with name as same trigger ID
        osc.retrieve_waveform_PC(source_folder, target_folder, id1)

    else:
        print("Wrong Trigger Mode Specified! Valid: SINGLE or NORMAL")
        