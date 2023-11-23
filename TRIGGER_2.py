# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:00:06 2023

@author: DAV1SI
"""
import time
from Oscilloscope_PyVisa import Oscilloscope
from SET_TRIGGER import SET_TRIGGER
import threading
from configparser import ConfigParser
import concurrent.futures
import pandas as pd

#Get the configparser object
config_object = ConfigParser()


#config parameters
ip = "192.168.40.26"
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
osc_path = "C:\\Users\LCRYDMIN\Desktop\\test" #there's a error. will debug it next week


if __name__ == "__main__":
    osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")

    # id = SET_TRIGGER(osc, trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path)  # There's some error with osc_path
    # print(f"\nTrigger ID =  {id}")
    start_time = time.time()

    settings_list = [[osc, 1, "C1", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test"],
                    [osc,  2, "C2", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test"], 
                [osc, 3, "C3", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test"], 
                [osc, 4, "C4", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test"]]


    # The ThreadPoolExecutor will automatically manage the threads, and the program will wait for all threads to finish

    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     executor.map(SET_TRIGGER, settings_list)

    # t1 = threading.Thread(target= SET_TRIGGER, args=(osc, 1, "C1", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test",))
    # t = threading.Lock()
    t2 = threading.Thread(target= SET_TRIGGER, args=(osc,  2, "C1", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test",))
    
    # t3 = threading.Thread(target=SET_TRIGGER, args=(osc, 3, "C1", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test",))

    # t4 = threading.Thread(target=SET_TRIGGER, args=(osc, 4, "C1", "EDGE", "SINGLE", "Positive", "DC", 10, "5US", 20, "C:\\Users\DAV1SI\Desktop\test",))


    # t1.start()
    # t.acquire()
    t2.start()
    # t3.start()
    # t4.start()
    

    # t1.join()
    t2.join()
    # t3.join()
    # t4.join()

    print("--- %s seconds ---" % round(time.time() - start_time, 4))