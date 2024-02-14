# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:15:26 2023

@author: DAV1SI

This script DEFINES SINGLE AND NORMAL trigger parameters of the oscilloscope and triggers, saves and retrieves the waveform

The data is saved on the controlling PC and OSC in .csv or .txt file formats with a specific trigger ID
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


def SET_SINGLE_TRIGGER(OSC, trace_status:dict, channel:str, trigger_slope:str, trigger_coupling:str, trigger_level:float, trig_delay:float, max_sample_pts:float): # OSC_path
        '''Set Trigger Parameters for Trigger Source'''
        OSC.set_trig_mode('AUTO')
        trig_source = channel
        OSC.set_trig_source(trig_source)
        OSC.set_trig_coupling(trig_source,trigger_coupling)
        OSC.set_trig_slope(trig_source,trigger_slope)
        OSC.set_trig_level(trig_source,trigger_level)
        OSC.set_trig_delay(trig_delay)
        
        print('Waiting for Trigger...')
        OSC.wait_for_single_trigger()
        # trigger_time = OSC.get_triggers_times(1)
        # print(f"Trigger Time = {trigger_time}")

        filename = str(OSC.trig_time().replace("," , "_"))
        OSC.show_measure("True")
        OSC.statistics_measure("True")
        PC_path	= r"C:\Users\DAV1SI\Desktop\test"                                                                                    #change according to your preferrred save folder on controlling PC

        '''Plot the waveforms of all channels & save them with parameters'''
        for i in range(1,9):                                                                                                         #set range(1,5) for 4-channel and range(1,9) for 8-channel Oscilloscope respectively
            trigger_id =  filename
            print(f"----------------TRIGGER ID: C{i} = {filename}-------------------------")
            
            waveform = OSC.get_waveform(i)
            waveform = pd.DataFrame(waveform)
    
            if waveform.empty == True: #or waveform.notna == True:
                  continue
            
            else:    
                # Plot the data
                plt.plot(waveform)
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude (V)')
                plt.title(f'C{i}: Acquired Waveform')
                # if trig_delay == 0.0:
                #         plt.axvline(x=0.5, color='g', linestyle='--', label='Trigger Point')
                # else:
                #         plt.axvline(x=trig_delay - 0.5, color='g', linestyle='--', label='Trigger Point')
                plt.axhline(y=trigger_level, color='b', linestyle='--', label='Trigger Level')
                plt.grid(True)
                plt.legend()
                plt.show()

                if trace_status[f"C{i}"] == "OFF":
                        continue
                else:
                        print(f'Saving C{i} waveform & parameters...\n')

                        # OSC.save_waveform_on_OSC("Excel", i,  "C" + str(i) + "_" + filename)
                        OSC.save_waveform_on_PC(PC_path, waveform,  "C" + str(i) + "_" + filename + "_waveform", max_sample_pts)
                        OSC.save_parameters_trace(PC_path, i, 'Excel', "C" + str(i) + "_" + filename + "_parameters")

                        print(f' C{i} waveform & parameters saved on PC\n')
                
        OSC.set_trig_mode("AUTO")
        print('Trigger Mode = AUTO\n')

        print('-------------------------------DONE!---------------------------------------')
        
        return trigger_id


def SET_NORMAL_TRIGGER(OSC, trace_status:dict, channel:str, trigger_slope:str, trigger_coupling:str, trigger_level:float, trig_delay:float, max_sample_pts:float):
        '''Set Trigger Parameters for Trigger Source'''
        OSC.set_trig_mode('AUTO')
        trig_source = channel
        OSC.set_trig_source(trig_source)
        OSC.set_trig_coupling(trig_source,trigger_coupling)
        OSC.set_trig_slope(trig_source,trigger_slope)
        OSC.set_trig_level(trig_source,trigger_level)
        OSC.set_trig_delay(trig_delay)
        
        print("Signal Triggering....")
        OSC.set_trig_source(channel)
        OSC.set_normal_trigger()
        filename = str(OSC.trig_time().replace("," , "_"))
        OSC.show_measure("True")
        OSC.statistics_measure("True")
        PC_path	= r"C:\Users\DAV1SI\Desktop\test"
        
        '''Plot the waveforms of all channels & save them with parameters'''
        for i in range(1,9):                                                                                                         #set range(1,5) for 4-channel and range(1,9) for 8-channel Oscilloscope respectively
                        trigger_id =  filename
                        print(f"----------------TRIGGER ID: C{i} = {filename}-------------------------")
                
                        waveform = OSC.get_waveform(i)
                        waveform = pd.DataFrame(waveform)
                                
                        if waveform.empty == True:# or waveform.notna == True:
                                continue
                        else:    
                                # Plot the data
                                plt.plot(waveform)
                                plt.xlabel('Time (s)')
                                plt.ylabel('Amplitude (V)')
                                plt.title(f'C{i}: Acquired Waveform')
                                # plt.axvline(x=trig_delay, color='g', linestyle='--', label='Trigger Point')
                                plt.axhline(y=trigger_level, color='b', linestyle='--', label='Trigger Level')
                                plt.grid(True)
                                plt.legend()
                                plt.show()

                                if trace_status[f"C{i}"] == "OFF":
                                        continue
                                else:
                                        print(f'Saving C{i} waveform & parameters...\n')

                                        # OSC.save_waveform_on_OSC("Excel", i,  "C" + str(i) + "_" + filename)
                                        OSC.save_waveform_on_PC(PC_path, waveform,  "C" + str(i) + "_" + filename + "_waveform", max_sample_pts)
                                        OSC.save_parameters_trace(PC_path, i, 'Excel', "C" + str(i) + "_" + filename + "_parameters")

                                        print(f' C{i} waveform & parameters saved on PC!\n')
                                
        print('-------------------------------DONE!---------------------------------------')
        return trigger_id      