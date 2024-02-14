import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import OptionMenu, StringVar
from Oscilloscope_PyVisa import Oscilloscope
import os
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import threading
from threading import Thread
import logging
import tkinter.scrolledtext as ScrolledText

import pandas as pd
from pandas import plotting
import numpy as np
import scipy.io as sio
from scipy.io import savemat
import time


global osc_connected
osc_connected = False
    
def set_level():
    e_text = level_entry.get()
    osc.set_trig_level(click_source.get(), float(e_text))  #%% Error 

def set_VerScale():
    entry = VerScale_value.get()
    osc.set_vdiv(1,float(entry))

def set_VerOff():
    entry = VerOff_value.get()
    osc.write(f"vbs? 'app.Acquisition.{click_source.get()}.VerOffset = {float(entry)}'")

def set_coupling():
    osc.set_trig_coupling(click_source.get(), click_coupling.get())

def set_units():
    osc.write(f"vbs? 'app.Acquisition.{click_source.get()}.Unit = {click_units.get()}'") # %% CHECK

def set_invert():
    if invert_status.get() == "ON":
        osc.query(f"vbs? 'app.Acquisition.{click_source.get()}.Invert = true'")
    else:
        osc.query(f"vbs? 'app.Acquisition.{click_source.get()}.Invert = false'")

def set_trace():
    if trace_status.get() == "OFF":
        osc.query(f"vbs? 'app.Acquisition.{click_source.get()}.View = false'")
    else:
        osc.query(f"vbs? 'app.Acquisition.{click_source.get()}.View = true'")

def set_slope():
    osc.set_trig_slope(click_source.get(), click_slope.get())

def set_trig_mode():
    osc.set_trig_mode(click_mode.get())
    TRIGGER_ID

def get_waveform():
    osc.get_waveform(click_mode.get())

def get_VerScale_value():
    osc.get_vdiv(click_mode.get())

def plot():
    plt.clf()
    data = osc.get_waveform(channel=int(click_source.get().split('C')[1])) #check
    #print(data)
    data = pd.DataFrame(data)
    ax.plot(data)
    osc.save_parameters_trace(int(click_source.get().split('C')[1]), 'Excel',  str("parameters_") + str(TRIGGER_ID(" ")))
    osc.save_waveform_on_OSC('Excel', int(click_source.get().split('C')[1]))
    osc.save_waveform_on_PC(data, str("waveform_") + str(TRIGGER_ID(" ")) + ".csv")
    plt.title("Acquired Waveform")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    canvas.draw()

def clear_waveform(): #CHECK
    plt.clf()

def _quit():        # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    root.quit()     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
         
def connect_oscilloscope(ip_address:str):
    osc = Oscilloscope(f'TCPIP0::{ip_address}::inst0::INSTR')
    osc.read_termination = '\n'
    osc.write_termination = '\n'
    osc_connected = True
    return osc

def TRIGGER_ID(filename): 
    trig_time = osc.query("DATE?")
    filename = '_Trigger-Type_' + str(click_type.get()) + '_Trigger-Mode_'+ str(click_mode.get()) + '_Trigger-Source_'+ str(click_source.get()) + '_Trigger-Coupling_'+ str(click_coupling.get())
    print(filename)
    return filename

def threading():
    t1 = Thread(target=plot).start()


# class TextHandler(logging.Handler):
#     # This class allows you to log to a Tkinter Text or ScrolledText widget
#     # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

#     def __init__(self, text):
#         # run the regular Handler __init__
#         logging.Handler.__init__(self)
#         # Store a reference to the Text it will log to
#         self.text = text

#     def emit(self, record):
#         msg = self.format(record)
#         def append():
#             self.text.configure(state='normal')
#             self.text.insert(tk.END, msg + '\n')
#             self.text.configure(state='disabled')
#             # Autoscroll to the bottom
#             self.text.yview(tk.END)
#         # This is necessary because we can't modify the Text from other threads
#         self.text.after(0, append)

# def worker():
#     # Skeleton worker function, runs in separate thread (see below)   
#     while True:
#         # Report time / date at 2-second intervals
#         time.sleep(2)
#         timeStr = time.asctime()
#         msg = 'Current time: ' + timeStr
#         logging.info(msg) 


options_channels = [1, 2, 3, 4, 5, 6, 7, 8]

options_channel_units = ['V','A','others']

options_t_div = ['1NS','2NS','5NS','10NS','20NS','50NS','100NS','200NS','500NS','1US','2US','5US','10US','20US','50US','100US','200US','500US','1MS','2MS','5MS','10MS','20MS','50MS','100MS','200MS','500MS','1S','2S','5S','10S','20S','50S','100S']

options_trig_sources = ['C1','C2','C3','C4', 'C5', 'C6', 'C7', 'C8', 'Ext','Line','FastEdge']

options_trig_types = ['EDGE', 'WIDTH', 'PATTERN', 'SMART', 'MEASUREMENT' , 'TV', 'MULTISTAGE']

options_trig_slopes = ["Positive", "Negative", "Either"]

options_trig_coupling = ['AC','DC','HFREJ','LFREJ']

options_trig_modes = ['AUTO', 'NORM', 'STOP', 'SINGLE']


if __name__ == '__main__':
    
    root = tk.Tk()
    style = ttk.Style()
    style.configure("Trigger.TButton", foreground='red', background = "white", font = "Segoe UI")
    
    # t1 = Thread(target=worker, args=[])
    # t1.start()

    osc = connect_oscilloscope("192.168.240.26")
  
    root.geometry('1600x1000')
    root.title(f"LeCroy Oscilloscope:{osc.idn}")
    #root.configure('fullscreen',True)
    root.configure(background="white",
                       highlightcolor="black", relief="flat", border=1, borderwidth=5)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(2, weight=1)

    click_units= StringVar()
    click_units.set(options_channel_units[0])
    
    click_t_div = StringVar()
    click_t_div.set(options_t_div[0])

    click_type = StringVar()
    click_type.set(options_trig_types[0])
    
    click_slope = StringVar()
    click_slope.set(options_trig_slopes[0])

    click_source = StringVar()
    click_source.set(options_trig_sources[0])

    click_coupling = StringVar()
    click_coupling.set(options_trig_coupling[0])

    click_mode = StringVar()
    click_mode.set(options_trig_modes[0])

    ip_address = StringVar()
    select_channel = tk.StringVar
    invert_status = tk.StringVar()
    trace_status = tk.StringVar()
    VerScale_value = tk.StringVar()
    VerOff_value = tk.StringVar()
    units_per_volt_value = tk.StringVar()
        
    # left frame widgets
    left_frame = ttk.Frame(root, border=4, borderwidth= 5, relief= 'raised', height=1000, width=600)
    left_frame.grid_rowconfigure(4, weight=1)
    left_frame.grid_columnconfigure(1, weight=1)
    
    # left frame layout
    left_frame.pack(side = tk.LEFT, fill = tk.BOTH, padx=5, pady=5)

    # #console log
    # console_frame = ttk.Frame(left_frame, border=4, borderwidth= 5, relief= 'raised', height=1000, width=600)
    # # Add text widget to display logging info
    # st = ScrolledText.ScrolledText(console_frame, state='disabled')
    # st.configure(font='TkFixedFont')
    # st.grid(column=0, row=3, sticky='w', columnspan=4)

    # # Create textLogger
    # text_handler = TextHandler(st)

    # # Logging configuration
    # logging.basicConfig(filename='test.log',
    #     level=logging.INFO, 
    #     format='%(asctime)s - %(levelname)s - %(message)s')        

    # # Add the handler to logger
    # logger = logging.getLogger()        
    # logger.addHandler(text_handler)

    # ================ DEVICE =========================================================
    device_frame = ttk.Frame(left_frame, relief='raised', border=4, borderwidth=5)
    device_frame.grid(column=0, row=0, padx=20, pady=20)
    
    device_label = ttk.Label(device_frame, text="Device", font=('Segoe UI', 14, 'bold'), anchor='w')
    device_label.grid(column=0, row=0)

    ip_label = ttk.Label(device_frame, text="IP:", font=("Segoe UI", 12))
    ip_label.grid(column=0, row=1)

    ip_entry = ttk.Entry(device_frame, textvariable = ip_address, width=20)
    ip_entry.grid(column=1, row=1, padx=10, pady=10)

    connection_status = ttk.Label(device_frame, text="Status: ")
    connection_status.grid(column=0, row=2)

    connect_button = ttk.Button(device_frame, text="Connect")
    connect_button.grid(row=3, column=0, padx=5, pady=5)

    disconnect_button = ttk.Button(device_frame, text="Disconnect")
    disconnect_button.grid(row=3, column=1, padx=5, pady=5)


    # ================ CHANNEL SETUP =========================================================
    channel_setup_frame = ttk.Label(left_frame, relief='raised', border=4, borderwidth=5)
    channel_setup_frame.grid(column=0, row=1, padx=20, pady=20)
    
    channel_setup_label = ttk.Label(channel_setup_frame, text='Channel Setup', font=('Segoe UI', 14, 'bold'), anchor='w')
    channel_setup_label.grid(column=0, row=1)

    #channel settings tabs
    channel_tabs = ttk.Notebook(channel_setup_frame)
    channel_tabs.grid(column=0, row=2, padx=10, pady=10)

    # ================ Connect Oscilloscope =========================================================    
    # connect_label = ttk.Label(master=left_frame, text= 'Status =', font=("Segoe UI", 14))
    # connect_label.grid(column=0, row=0)
    # connect_button = ttk.Button(master=left_frame, text='Connect' ,command = connect_oscilloscope('192.168.40.26'))
    # connect_button.grid(column=1, row=0)

    while True:
        for i in range(1,5):
            # ================ CHANNEL =========================================================

            # ch widgets
            frame = ttk.Frame(channel_tabs)
            frame.grid_rowconfigure(0, weight=0)
            frame.grid_columnconfigure(0, weight=0)
            frame['padding'] = (5,10,5,10)
            
            label = ttk.Label(frame, text= str("C") + str(options_channels[i-1]), font=("Segoe UI", 14, 'bold'))
            trace_button = ttk.Checkbutton(frame, text='Trace On', variable=trace_status, onvalue='ON', offvalue='OFF', command= set_trace)
            VerScale_label = ttk.Label(frame, text='Vertical Scale:', font=("Segoe UI", 12))
            VerScale_entry = ttk.Entry(frame, textvariable = VerScale_value, width=10)
            VerScale_button = ttk.Button(frame, text="Set", command = lambda: osc.set_vdiv(i, float(VerScale_value.get())))
            current_VerScale = ttk.Label(frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.get_vdiv(i)).start)) #CHECK

            VerOff_label = ttk.Label(frame, text='Offset:', font=("Segoe UI", 12))
            VerOff_entry = ttk.Entry(frame, textvariable = VerOff_value, width=10)
            VerOff_button = ttk.Button(frame, text="Set", command = set_VerOff)
            current_VerOff = ttk.Label(frame, width=8, borderwidth=2, relief="groove")

            #drop_channel = OptionMenu(frame, click_channel, *options_channels)
            tdiv_label = ttk.Label(frame, text='Time/div:', font=("Segoe UI", 12))
            drop_t_div = OptionMenu(frame, click_t_div, *options_t_div, command = osc.set_tdiv)
            current_t_div = ttk.Label(frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.query("tdiv?")).start)) #CHECK
        
            rescale_label = ttk.Label(frame, text='Rescale:', font=("Segoe UI", 14, 'bold'))
            Units_label = ttk.Label(frame, text='Vertical Unit:', font=("Segoe UI", 12))
            Units_drop = OptionMenu(frame, click_units, *options_channel_units, command= set_units)
            current_units = ttk.Label(frame, width=8, borderwidth=2, relief="groove")  

            units_per_volt_label = ttk.Label(frame, text='Units /V (slope):', font=("Segoe UI", 12))
            units_per_volt_entry = ttk.Entry(frame, textvariable = units_per_volt_value, width=10)
            units_per_volt_button = ttk.Button(frame, text="Set", command = lambda: osc.set_units_per_volt(i, float(units_per_volt_value.get())))
            current_units_per_volt = ttk.Label(frame, width=8, borderwidth=2, relief="groove")

            # ================= CH layout ====================================================================
            frame.pack(fill = tk.BOTH, expand = 1, padx = 5, pady = 5)
            label.grid(column=2, row=0)
            VerScale_label.grid(column=5, row=2)
            VerScale_entry.grid(column=6, row=2)
            VerScale_button.grid(column=7, row=2)
            current_VerScale.grid(column=8, row=2)
            VerOff_label.grid(column=5, row=3)
            VerOff_entry.grid(column=6, row=3)
            current_VerOff.grid(column=8, row=3)
            VerOff_button.grid(column=7, row=3)
            tdiv_label.grid(column=5, row=4)
            drop_t_div.grid(column=6, row=4)
            current_t_div.grid(column=7, row=4)
            trace_button.grid(column=5, row=5)
            rescale_label.grid(column=11, row=0)
            Units_label.grid(column=13, row=2)
            Units_drop.grid(column=14, row=2)
            current_units.grid(column=15, row=2)
            units_per_volt_label.grid(column=13, row=3)
            units_per_volt_entry.grid(column=14, row=3)
            units_per_volt_button.grid(column=15, row=3)
            current_units_per_volt.grid(column=16, row=3)
            
            channel_tabs.add(frame, text=str(options_channels[i-1]))
        



    # # ================ CHANNEL 1 =========================================================

    # # ch 1 widgets
    # ch1_frame = ttk.Frame(channel_tabs)
    # ch1_frame.grid_rowconfigure(0, weight=0)
    # ch1_frame.grid_columnconfigure(0, weight=0)
    # ch1_frame['padding'] = (5,10,5,10)
    
    # ch1_label = ttk.Label(ch1_frame, text='C1:', font=("Segoe UI", 14, 'bold'))
    # ch1_trace_button = ttk.Checkbutton(ch1_frame, text='Trace On', variable=trace_status, onvalue='ON', offvalue='OFF', command= set_trace)
    # ch1_VerScale_label = ttk.Label(ch1_frame, text='Vertical Scale:', font=("Segoe UI", 12))
    # ch1_VerScale_entry = ttk.Entry(ch1_frame, textvariable = VerScale_value, width=10)
    # ch1_VerScale_button = ttk.Button(ch1_frame, text="Set", command = lambda: osc.set_vdiv(1, float(VerScale_value.get())))
    # ch1_current_VerScale = ttk.Label(ch1_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.get_vdiv(1)).start)) #CHECK

    # ch1_VerOff_label = ttk.Label(ch1_frame, text='Offset:', font=("Segoe UI", 12))
    # ch1_VerOff_entry = ttk.Entry(ch1_frame, textvariable = VerOff_value, width=10)
    # ch1_VerOff_button = ttk.Button(ch1_frame, text="Set", command = set_VerOff)
    # ch1_current_VerOff = ttk.Label(ch1_frame, width=8, borderwidth=2, relief="groove")

    # #drop_channel = OptionMenu(ch1_frame, click_channel, *options_channels)
    # ch1_tdiv_label = ttk.Label(ch1_frame, text='Time/div:', font=("Segoe UI", 12))
    # ch1_drop_t_div = OptionMenu(ch1_frame, click_t_div, *options_t_div, command = osc.set_tdiv)
    # ch1_current_t_div = ttk.Label(ch1_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.query("tdiv?")).start)) #CHECK
 
    # ch1_rescale_label = ttk.Label(ch1_frame, text='Rescale:', font=("Segoe UI", 14, 'bold'))
    # ch1_Units_label = ttk.Label(ch1_frame, text='Vertical Unit:', font=("Segoe UI", 12))
    # ch1_Units_drop = OptionMenu(ch1_frame, click_units, *options_channel_units, command= set_units())
    # ch1_current_units = ttk.Label(ch1_frame, width=8, borderwidth=2, relief="groove")  

    # ch1_units_per_volt_label = ttk.Label(ch1_frame, text='Units /V (slope):', font=("Segoe UI", 12))
    # ch1_units_per_volt_entry = ttk.Entry(ch1_frame, textvariable = units_per_volt_value, width=10)
    # ch1_units_per_volt_button = ttk.Button(ch1_frame, text="Set", command = lambda: osc.set_units_per_volt(1, float(units_per_volt_value.get())))
    # ch1_current_units_per_volt = ttk.Label(ch1_frame, width=8, borderwidth=2, relief="groove")

    # # ================= CH1 layout ====================================================================
    # ch1_frame.pack(fill = tk.BOTH, expand = 1, padx = 5, pady = 5)
    # ch1_label.grid(column=2, row=0)
    # ch1_VerScale_label.grid(column=5, row=2)
    # ch1_VerScale_entry.grid(column=6, row=2)
    # ch1_VerScale_button.grid(column=7, row=2)
    # ch1_current_VerScale.grid(column=8, row=2)
    # ch1_VerOff_label.grid(column=5, row=3)
    # ch1_VerOff_entry.grid(column=6, row=3)
    # ch1_current_VerOff.grid(column=8, row=3)
    # ch1_VerOff_button.grid(column=7, row=3)
    # ch1_tdiv_label.grid(column=5, row=4)
    # ch1_drop_t_div.grid(column=6, row=4)
    # ch1_current_t_div.grid(column=7, row=4)
    # ch1_trace_button.grid(column=5, row=5)
    # ch1_rescale_label.grid(column=11, row=0)
    # ch1_Units_label.grid(column=13, row=2)
    # ch1_Units_drop.grid(column=14, row=2)
    # ch1_current_units.grid(column=15, row=2)
    # ch1_units_per_volt_label.grid(column=13, row=3)
    # ch1_units_per_volt_entry.grid(column=14, row=3)
    # ch1_units_per_volt_button.grid(column=15, row=3)
    # ch1_current_units_per_volt.grid(column=16, row=3)
    
    
    # # ================ CHANNEL 2 =========================================================

    # # ch 2 widgets
    # ch2_frame = ttk.Frame(channel_tabs)
    # ch2_frame.grid_rowconfigure(0, weight=0)
    # ch2_frame.grid_columnconfigure(0, weight=0)
    # ch2_frame['padding'] = (5,10,5,10)
    
    # ch2_label = ttk.Label(ch2_frame, text='C2:', font=("Segoe UI", 14, 'bold'))
    # ch2_trace_button = ttk.Checkbutton(ch2_frame, text='Trace On', variable=trace_status, onvalue='ON', offvalue='OFF', command= set_trace)

    # ch2_VerScale_label = ttk.Label(ch2_frame, text='Vertical Scale:', font=("Segoe UI", 12))
    # ch2_VerScale_entry = ttk.Entry(ch2_frame, textvariable = VerScale_value, width=10)
    # ch2_VerScale_button = ttk.Button(ch2_frame, text="Set", command = lambda: osc.set_vdiv(2, float(VerScale_value.get())))
    # ch2_current_VerScale = ttk.Label(ch2_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.get_vdiv(2)).start)) #CHECK

    # ch2_VerOff_label = ttk.Label(ch2_frame, text='Offset:', font=("Segoe UI", 12))
    # ch2_VerOff_entry = ttk.Entry(ch2_frame, textvariable = VerOff_value, width=10)
    # ch2_VerOff_button = ttk.Button(ch2_frame, text="Set", command = set_VerOff)
    # ch2_current_VerOff = ttk.Label(ch2_frame, width=8, borderwidth=2, relief="groove")

    # ch2_tdiv_label = ttk.Label(ch2_frame, text='Time/div:', font=("Segoe UI", 12))
    # ch2_drop_t_div = OptionMenu(ch2_frame, click_t_div, *options_t_div, command = osc.set_tdiv)
    # ch2_current_t_div = ttk.Label(ch2_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.query("tdiv?")).start)) #CHECK
 
    # ch2_rescale_label = ttk.Label(ch2_frame, text='Rescale:', font=("Segoe UI", 14, 'bold'))
    # ch2_Units_label = ttk.Label(ch2_frame, text='Vertical Unit:', font=("Segoe UI", 12))
    # ch2_Units_drop = OptionMenu(ch2_frame, click_units, *options_channel_units, command= set_units())
    # ch2_current_units = ttk.Label(ch2_frame, width=8, borderwidth=2, relief="groove")  

    # ch2_units_per_volt_label = ttk.Label(ch2_frame, text='Units /V (slope):', font=("Segoe UI", 12))
    # ch2_units_per_volt_entry = ttk.Entry(ch2_frame, textvariable = units_per_volt_value, width=10)
    # ch2_units_per_volt_button = ttk.Button(ch2_frame, text="Set", command = lambda: osc.set_units_per_volt(2, float(units_per_volt_value.get())))
    # ch2_current_units_per_volt = ttk.Label(ch2_frame, width=8, borderwidth=2, relief="groove")

    # # ================= CH2 layout ====================================================================
    # ch2_frame.pack(fill = tk.BOTH, expand = 1, padx = 5, pady = 5)
    # ch2_label.grid(column=2, row=0)
    # ch2_VerScale_label.grid(column=5, row=2)
    # ch2_VerScale_entry.grid(column=6, row=2)
    # ch2_VerScale_button.grid(column=7, row=2)
    # ch2_current_VerScale.grid(column=8, row=2)
    # ch2_VerOff_label.grid(column=5, row=3)
    # ch2_VerOff_entry.grid(column=6, row=3)
    # ch2_current_VerOff.grid(column=8, row=3)
    # ch2_VerOff_button.grid(column=7, row=3)
    # ch2_tdiv_label.grid(column=5, row=4)
    # ch2_drop_t_div.grid(column=6, row=4)
    # ch2_current_t_div.grid(column=7, row=4)
    # ch2_trace_button.grid(column=5, row=5)
    # ch2_rescale_label.grid(column=11, row=0)
    # ch2_Units_label.grid(column=13, row=2)
    # ch2_Units_drop.grid(column=14, row=2)
    # ch2_current_units.grid(column=15, row=2)
    # ch2_units_per_volt_label.grid(column=13, row=3)
    # ch2_units_per_volt_entry.grid(column=14, row=3)
    # ch2_units_per_volt_button.grid(column=15, row=3)
    # ch2_current_units_per_volt.grid(column=16, row=3)

    #  # ================ CHANNEL 3 =========================================================

    # # ch 3 widgets
    # ch3_frame = ttk.Frame(channel_tabs)
    # ch3_frame.grid_rowconfigure(0, weight=0)
    # ch3_frame.grid_columnconfigure(0, weight=0)
    # ch3_frame['padding'] = (5,10,5,10)
    
    # ch3_label = ttk.Label(ch3_frame, text='C3:', font=("Segoe UI", 14, 'bold'))
    # ch3_trace_button = ttk.Checkbutton(ch3_frame, text='Trace On', variable=trace_status, onvalue='ON', offvalue='OFF', command= set_trace)

    # ch3_VerScale_label = ttk.Label(ch3_frame, text='Vertical Scale:', font=("Segoe UI", 12))
    # ch3_VerScale_entry = ttk.Entry(ch3_frame, textvariable = VerScale_value, width=10)
    # ch3_VerScale_button = ttk.Button(ch3_frame, text="Set", command = lambda: osc.set_vdiv(3, float(VerScale_value.get())))
    # ch3_current_VerScale = ttk.Label(ch3_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.get_vdiv(3)).start)) #CHECK

    # ch3_VerOff_label = ttk.Label(ch3_frame, text='Offset:', font=("Segoe UI", 12))
    # ch3_VerOff_entry = ttk.Entry(ch3_frame, textvariable = VerOff_value, width=10)
    # ch3_VerOff_button = ttk.Button(ch3_frame, text="Set", command = set_VerOff)
    # ch3_current_VerOff = ttk.Label(ch3_frame, width=8, borderwidth=2, relief="groove")

    # ch3_tdiv_label = ttk.Label(ch3_frame, text='Time/div:', font=("Segoe UI", 12))
    # ch3_drop_t_div = OptionMenu(ch3_frame, click_t_div, *options_t_div, command = osc.set_tdiv)
    # ch3_current_t_div = ttk.Label(ch3_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.query("tdiv?")).start)) #CHECK
 
    # ch3_rescale_label = ttk.Label(ch3_frame, text='Rescale:', font=("Segoe UI", 14, 'bold'))
    # ch3_Units_label = ttk.Label(ch3_frame, text='Vertical Unit:', font=("Segoe UI", 12))
    # ch3_Units_drop = OptionMenu(ch3_frame, click_units, *options_channel_units, command= set_units())
    # ch3_current_units = ttk.Label(ch3_frame, width=8, borderwidth=2, relief="groove")  

    # ch3_units_per_volt_label = ttk.Label(ch3_frame, text='Units /V (slope):', font=("Segoe UI", 12))
    # ch3_units_per_volt_entry = ttk.Entry(ch3_frame, textvariable = units_per_volt_value, width=10)
    # ch3_units_per_volt_button = ttk.Button(ch3_frame, text="Set", command = lambda: osc.set_units_per_volt(3, float(units_per_volt_value.get())))
    # ch3_current_units_per_volt = ttk.Label(ch3_frame, width=8, borderwidth=2, relief="groove")

    # # ================= CH3 layout ====================================================================
    # ch3_frame.pack(fill = tk.BOTH, expand = 1, padx = 5, pady = 5)
    # ch3_label.grid(column=2, row=0)
    # ch3_VerScale_label.grid(column=5, row=2)
    # ch3_VerScale_entry.grid(column=6, row=2)
    # ch3_VerScale_button.grid(column=7, row=2)
    # ch3_current_VerScale.grid(column=8, row=2)
    # ch3_VerOff_label.grid(column=5, row=3)
    # ch3_VerOff_entry.grid(column=6, row=3)
    # ch3_current_VerOff.grid(column=8, row=3)
    # ch3_VerOff_button.grid(column=7, row=3)
    # ch3_tdiv_label.grid(column=5, row=4)
    # ch3_drop_t_div.grid(column=6, row=4)
    # ch3_current_t_div.grid(column=7, row=4)
    # ch3_trace_button.grid(column=5, row=5)
    # ch3_rescale_label.grid(column=11, row=0)
    # ch3_Units_label.grid(column=13, row=2)
    # ch3_Units_drop.grid(column=14, row=2)
    # ch3_current_units.grid(column=15, row=2)
    # ch3_units_per_volt_label.grid(column=13, row=3)
    # ch3_units_per_volt_entry.grid(column=14, row=3)
    # ch3_units_per_volt_button.grid(column=15, row=3)
    # ch3_current_units_per_volt.grid(column=16, row=3)

    # # ================ CHANNEL 4 =========================================================

    # # ch 4 widgets
    # ch4_frame = ttk.Frame(channel_tabs)
    # ch4_frame.grid_rowconfigure(0, weight=0)
    # ch4_frame.grid_columnconfigure(0, weight=0)
    # ch4_frame['padding'] = (5,10,5,10)
    
    # ch4_label = ttk.Label(ch4_frame, text='C4:', font=("Segoe UI", 14, 'bold'))
    # ch4_trace_button = ttk.Checkbutton(ch4_frame, text='Trace On', variable=trace_status, onvalue='ON', offvalue='OFF', command= set_trace)

    # ch4_VerScale_label = ttk.Label(ch4_frame, text='Vertical Scale:', font=("Segoe UI", 12))
    # ch4_VerScale_entry = ttk.Entry(ch4_frame, textvariable = VerScale_value, width=10)
    # ch4_VerScale_button = ttk.Button(ch4_frame, text="Set", command = lambda: osc.set_vdiv(4, float(VerScale_value.get())))
    # ch4_current_VerScale = ttk.Label(ch4_frame, width=8, borderwidth=2, relief="groove", text= str(Thread(target=osc.get_vdiv(4)).start())) #CHECK

    # ch4_VerOff_label = ttk.Label(ch4_frame, text='Offset:', font=("Segoe UI", 12))
    # ch4_VerOff_entry = ttk.Entry(ch4_frame, textvariable = VerOff_value, width=10)
    # ch4_VerOff_button = ttk.Button(ch4_frame, text="Set", command = set_VerOff)
    # ch4_current_VerOff = ttk.Label(ch4_frame, width=8, borderwidth=2, relief="groove")

    # ch4_tdiv_label = ttk.Label(ch4_frame, text='Time/div:', font=("Segoe UI", 12))
    # ch4_drop_t_div = OptionMenu(ch4_frame, click_t_div, *options_t_div, command = osc.set_tdiv)
    # ch4_current_t_div = ttk.Label(ch4_frame, width=8, borderwidth=2, relief="groove", text= str(osc.query("tdiv?"))) #CHECK
 
    # ch4_rescale_label = ttk.Label(ch4_frame, text='Rescale:', font=("Segoe UI", 14, 'bold'))
    # ch4_Units_label = ttk.Label(ch4_frame, text='Vertical Unit:', font=("Segoe UI", 12))
    # ch4_Units_drop = OptionMenu(ch4_frame, click_units, *options_channel_units, command= set_units())
    # ch4_current_units = ttk.Label(ch4_frame, width=8, borderwidth=2, relief="groove")  

    # ch4_units_per_volt_label = ttk.Label(ch4_frame, text='Units /V (slope):', font=("Segoe UI", 12))
    # ch4_units_per_volt_entry = ttk.Entry(ch4_frame, textvariable = units_per_volt_value, width=10)
    # ch4_units_per_volt_button = ttk.Button(ch4_frame, text="Set", command = lambda: osc.set_units_per_volt(4, float(units_per_volt_value.get())))
    # ch4_current_units_per_volt = ttk.Label(ch4_frame, width=8, borderwidth=2, relief="groove")

    # # ================= CH4 layout ====================================================================
    # ch4_frame.pack(fill = tk.BOTH, expand = 1, padx = 5, pady = 5)
    # ch4_label.grid(column=2, row=0)
    # ch4_VerScale_label.grid(column=5, row=2)
    # ch4_VerScale_entry.grid(column=6, row=2)
    # ch4_VerScale_button.grid(column=7, row=2)
    # ch4_current_VerScale.grid(column=8, row=2)
    # ch4_VerOff_label.grid(column=5, row=3)
    # ch4_VerOff_entry.grid(column=6, row=3)
    # ch4_current_VerOff.grid(column=8, row=3)
    # ch4_VerOff_button.grid(column=7, row=3)
    # ch4_tdiv_label.grid(column=5, row=4)
    # ch4_drop_t_div.grid(column=6, row=4)
    # ch4_current_t_div.grid(column=7, row=4)
    # ch4_trace_button.grid(column=5, row=5)
    # ch4_rescale_label.grid(column=11, row=0)
    # ch4_Units_label.grid(column=13, row=2)
    # ch4_Units_drop.grid(column=14, row=2)
    # ch4_current_units.grid(column=15, row=2)
    # ch4_units_per_volt_label.grid(column=13, row=3)
    # ch4_units_per_volt_entry.grid(column=14, row=3)
    # ch4_units_per_volt_button.grid(column=15, row=3)
    # ch4_current_units_per_volt.grid(column=16, row=3)

        # ================= TRIGGER SETUP  ====================================================================
        
        # bottom left frame widgets
        bottom_frame = ttk.Frame(left_frame, relief='raised', border=4, borderwidth=5)
        trig_label = ttk.Label(bottom_frame, text='Trigger Setup:', font=("Segoe UI", 14, 'bold'))

        trig_type_label = ttk.Label(bottom_frame, text='Type:', font=("Segoe UI", 12))
        drop_trig_types = OptionMenu(bottom_frame, click_type, *options_trig_types, command = osc.set_trig_type)

        source_label = ttk.Label(bottom_frame, text='Source:', font=("Segoe UI", 12))
        drop_sources = OptionMenu(bottom_frame, click_source, *options_trig_sources, command=osc.set_trig_source)

        coupling_label = ttk.Label(bottom_frame, text='Coupling:', font=("Segoe UI", 12))
        drop_coupling = OptionMenu(bottom_frame, click_coupling, *options_trig_coupling)
        coupling_button = ttk.Button(bottom_frame, text="Set", command = set_coupling)
        
        slope_label = ttk.Label(bottom_frame, text='Slope:', font=("Segoe UI", 12))
        drop_slope = OptionMenu(bottom_frame, click_slope, *options_trig_slopes)
        slope_button = ttk.Button(bottom_frame, text="Set", command = set_slope)

        invert_button = ttk.Checkbutton(bottom_frame, text='Invert', variable=invert_status, onvalue='ON', offvalue='OFF', command=set_invert)   

        level_entry = ttk.Entry(bottom_frame, width=10)
        level_label = ttk.Label(bottom_frame, text='Level:', font=("Segoe UI", 12))
        set_level_button = ttk.Button(bottom_frame, text="Set Level", command = set_level)
        drop_modes = OptionMenu(bottom_frame, click_mode, *options_trig_modes)
        trigger_button = ttk.Button(bottom_frame, text="Trigger", style="TButton",command = set_trig_mode)

        # bottom frame (left)  layout
        bottom_frame.grid(column=0, row=3, padx=20, pady=20)
        trig_label.grid(column=0, row=0)
        trig_type_label.grid(column=0, row=5)
        drop_trig_types.grid(column=1, row=5)
        source_label.grid(column=3, row=5)
        drop_sources.grid(column=4, row=5)
        coupling_label.grid(column=3, row=7)
        drop_coupling.grid(column=4, row=7)
        coupling_button.grid(column=5, row=7)
        slope_label.grid(column=3, row=9)
        drop_slope.grid(column=4, row=9)
        slope_button.grid(column=5, row=9)

        level_label.grid(column=6, row=5)
        level_entry.grid(column=7, row=5)
        set_level_button.grid(column=8, row=5)
        drop_modes.grid(column=6, row=13)
        trigger_button.grid(column=7, row=13)
        invert_button.grid(column=3, row=20)


        # =================STATUS WINDOW  ====================================================================

        # status_frame = ttk.Frame(left_frame)
        # status_frame.grid(row=4, column=0)
        
        # status = ttk.Label(status_frame, text="Status:" + str(osc_connected) , border=1, relief='sunken') #CHECK
        # status.grid(row=4, column=0, columnspan=5)

        # =================TERMINAL WINDOW  ====================================================================
        # termf = ttk.Frame(status_frame, height=100, width=100, relief='sunken')
        # termf.grid(column=0, row=3)
        # wid = termf.winfo_id()
        # os.system('xterm -into %d -geometry 40x20 -sb &' % wid)
        
        # #tabs
        # channel_tabs.add(ch1_frame, text='C1')
        # channel_tabs.add(ch2_frame, text='C2')
        # channel_tabs.add(ch3_frame, text='C3')
        # channel_tabs.add(ch4_frame, text='C4')
    
        # right frame
        right_frame = ttk.Frame(root) 
        
        # right frame layout
        right_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1, padx = 5, pady = 5)
            
        fig = matplotlib.figure.Figure()
        ax = fig.add_subplot()    
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.get_tk_widget().pack(fill='both', expand=1)
    
        toolbar = NavigationToolbar2Tk(canvas, right_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(anchor = "w", fill=tk.X)

        #plot_button = ttk.Button(right_frame, text='Get Waveform', command= plot)
        #plot_button.pack()

        # clear_waveform_button = ttk.Button(right_frame, text='Clear', command=clear_waveform)
        # clear_waveform_button.pack(side='right')

        download_button = tk.Button(master=right_frame, text="Save Data", command = threading) #Check RunTime Error
        download_button.pack()

        quit_button = tk.Button(master=right_frame, text="Quit", command=_quit)
        quit_button.pack()

        root.mainloop()
        # t1.join()
        


        
        