from Oscilloscope_PyVisa import Oscilloscope
#from GUI import TRIGGER_ID
import pandas as pd

#This script triggers the signals and saves the Waveform data and measured parameters in excel files on the PC.
#The waveform data is also stored on the oscilloscope

ip = "192.168.40.26"
trig_source = "C2"
channel = 2

OSCI = Oscilloscope(f"TCPIP0::{ip}::inst0::INSTR")
OSCI.set_trig_source(trig_source)
waveform = OSCI.get_waveform(channel)
waveform = pd.DataFrame(waveform)
OSCI.save_waveform_on_PC(waveform, "test_waveform.csv")
OSCI.save_waveform_on_OSC("Excel", channel)
OSCI.save_parameters_trace(channel, "Excel", "test_para.csv")