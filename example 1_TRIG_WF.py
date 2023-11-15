from Oscilloscope_PyVisa import Oscilloscope
#from GUI import *
from GUI import TRIGGER_ID
#This script sets the channel & trigger parameters of the oscilloscope and triggers and receives the waveform

ip = "192.168.40.100"

channel = 4
trig_source = "C4"
trig_type = 'EDGE'
trig_coupling = 'DC'
trig_slope = 'Positive'
trig_mode = 'SINGLE'
filename = '_Trigger-Source_' + str(trig_source)  + '_Type_' + str(trig_type) + '_Mode_'+ str(trig_mode) + '_Slope_'+ str(trig_slope) + '_Coupling_'+ str(trig_coupling)

osc = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")
osc.set_tdiv("10US")
osc.set_vdiv(channel, 20)
osc.set_trig_source(trig_source)
osc.set_trig_type('EDGE')
osc.set_trig_coupling(trig_source,"DC")
osc.set_trig_slope(trig_source,"Positive")
osc.set_trig_level(trig_source,1)
osc.set_trig_mode("SINGLE")
trig_time = osc.query("DATE?")
TRIGGER_ID(str(trig_time) + str(filename))
data = osc.get_waveform(channel)
print(data)