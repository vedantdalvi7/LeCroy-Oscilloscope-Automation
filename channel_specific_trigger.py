from Oscilloscope_PyVisa import Oscilloscope
from SET_TRIGGER import SET_TRIGGER
import threading

#config parameters
ip = "192.168.40.26"
channel = 2
tdiv = "20US"
vdiv = 10
trig_source = "C2"
trig_type = 'EDGE'
trig_coupling = 'DC'
trig_slope = 'Positive'
trig_mode = 'SINGLE'
trig_level = 5
pc_path = "C:\\Users\DAV1SI\Desktop\test"
osc_path = "C:\\Users\LCRYDMIN\Desktop\test" #there's a error. will debug it next week

osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")
t2 = threading.Thread(target=SET_TRIGGER(osc, channel, trig_source, trig_type, trig_mode, trig_slope, trig_coupling, trig_level, tdiv, vdiv, pc_path))

t2.start()

t2.join()