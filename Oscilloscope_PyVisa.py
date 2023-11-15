import pyvisa as visa
# import matplotlib.pyplot as plt
import pandas as pd

import xlsxwriter
# from xlsxwriter import Workbook
import time
import numpy as np
import datetime

import os
# import csv
# from csv import writer

# import xlsxwriter

connected = False

   
def _validate_channel_number(channel):
    CHANNEL_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8}
    if channel not in CHANNEL_NUMBERS:
        raise ValueError(f'<channel> must be in {CHANNEL_NUMBERS}')
    
def _validate_t_div_value(t_div_value):
    T_DIV_VALID = {'1NS','2NS','5NS','10NS','20NS','50NS','100NS','200NS','500NS','1US','2US','5US','10US','20US','50US','100US','200US','500US','1MS','2MS','5MS','10MS','20MS','50MS','100MS','200MS','500MS','1S','2S','5S','10S','20S','50S','100S'}
    if not isinstance(t_div_value, str):
        raise TypeError(f'The times/div must be a string, received object of type {type(t_div_value)}.')
    if t_div_value.lower() not in {t.lower() for t in T_DIV_VALID}:
        raise ValueError(f'The times/div must be one of {T_DIV_VALID}, received {repr(t_div_value)}...')
    
def _validate_trig_source(trig_source):
    TRIG_SOURCES_VALID = {'C1','C2','C3','C4', 'C5', 'C6', 'C7', 'C8', 'Ext','Line','FastEdge'}
    if not isinstance(trig_source, str):
        raise TypeError(f'The trigger source must be a string, received object of type {type(trig_source)}.')
    if trig_source.lower() not in {t.lower() for t in TRIG_SOURCES_VALID}:
        raise ValueError(f'The trigger source must be one of {TRIG_SOURCES_VALID}, received {repr(trig_source)}...')
    
def _validate_trig_type(trig_type):
    TRIG_TYPES_VALID = {'EDGE', 'WIDTH', 'PATTERN', 'SMART', 'MEASUREMENT' , 'TV', 'MULTISTAGE'}
    if not isinstance(trig_type, str):
        raise TypeError(f'The trigger type must be a string, received object of type {type(trig_type)}.')
    if trig_type.lower() not in {t.lower() for t in TRIG_TYPES_VALID}:
        raise ValueError(f'The trigger source must be one of {TRIG_TYPES_VALID}, received {repr(trig_type)}...')
    
def _validate_waveform_format(format:str):
    FORMAT_NAMES_VALID= {'Binary','ASCII','Excel','MATLAB','MathCad'}
    if not isinstance(format, str):
        raise TypeError(f'The format type must be a string, received ibject of type {type(format)}')
    if format.lower() not in {t.lower() for t in FORMAT_NAMES_VALID}:
        raise ValueError(f'<FORMAT> must be one of {FORMAT_NAMES_VALID},  received {repr(format)}...')
    
class Oscilloscope:
    def __init__(self, resource_name:str):
        """This is a wrapper class for a pyvisa Resource object to communicate
        with a LeCroy oscilloscope.
        
        Parameters
        ----------
        resource_name: str
            Whatever you have to provide to `pyvisa` to open the connection
            with the oscilloscope, see [here](https://pyvisa.readthedocs.io/en/latest/api/resourcemanager.html#pyvisa.highlevel.ResourceManager.open_resource).
            Example: "USB0::0x05ff::0x1023::4751N40408::INSTR"
        """
        
        global connected
        
        if not isinstance(resource_name, str):
            raise TypeError(f'<resource_name> must be a string, received object of type {type(resource_name)}')
        
        try:
            oscilloscope = visa.ResourceManager('@ivi').open_resource(resource_name)
            connected = True
            print(f"Connection to Oscilloscope {resource_name} successfull \n")
        except visa.errors.VisaIOError:
            try:
                visa.ResourceManager('@py').open_resource(resource_name) 
                connected = True
                print(f"Connection to Oscilloscope {resource_name} successfull \n")
            except:
                connected = False
                pass
            oscilloscope = visa.ResourceManager('@ivi').open_resource(resource_name)
        except OSError as e:
            if 'Could not open VISA library' in str(e):
                oscilloscope = visa.ResourceManager('@py').open_resource(resource_name)
                connected = False
            else:
                raise e
                connected = False
        
        self.resource = oscilloscope
        self.write('CHDR OFF') # This is to receive only numerical data in the answers and not also the echo of the command and some other stuff. See p. 22 of http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf
        if 'lecroy' not in self.idn.lower():
            raise RuntimeError(f'The instrument you provided does not seem to be a LeCroy oscilloscope, its name is {self.idn}. Please check this.')


    @property
    def idn(self):
        """Returns the name of the instrument, i.e. its answer to the
        command "*IDN?"."""
        return  self.query('*IDN?')
    
    def trig_time(self):
        """Returns the date and time of the instrument, i.e. when the waveform was triggered."""
        return  self.query('DATE?')
    
    def write(self, msg):
        """Sends a command to the instrument."""
        self.resource.write(msg)
    
    def read(self):
        """Reads the answer from the instrument."""
        response = self.resource.read()
        if response[-1] == '\n':
            response = response[:-1]
        return response
    
    def query(self, msg):
        """Sends a command to the instrument and immediately reads the
        answer."""
        self.write(msg)
        time.sleep(0.5)
        return self.read()
    
    def get_waveform(self, channel: int):
        """Gets the waveform from the specified channel.
        
        Arguments
        ---------
        channel: int
            Number of channel from which to get the waveform data.
        
        Returns
        -------
        waveform(s): dict or list
            If the "sampling mode" is not "Sequence", a dictionary of the 
            form `{'Time (s)': numpy.array, 'Amplitude (V)': numpy.array}`
            is returned with the waveform.
            If "sampling mode" "Sequence" is configured in the oscilloscope
            then a list of dictionaries is returned, each element of the
            list being each waveform from each sequence.
        """
        _validate_channel_number(channel)
        
        # Page 223: http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf
        # Page 258: http://cdn.teledynelecroy.com/files/manuals/wr2_rcm_revb.pdf
        self.write(f'C{channel}:WF?')
        raw_data = list(self.resource.read_raw())
        
        seq = self.query('SEQUENCE?')
        sequence_status = seq.split(',')[0]
        n_segments_configured = int(seq.split(',')[1])
        n_segments_acquired = 0 if sequence_status=='OFF' else int(self.query("VBS? 'return=app.Acquisition.Horizontal.AcquiredSegments'")) # See https://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf p. 1-20.
        
        raw_data = raw_data[:-1] # For some reason last sample always seems to be some random garbage.
        raw_data = raw_data[16*(n_segments_acquired)+361:] # Here I drop the first "n" samples which are garbage, same as the last one. Don't know the reason for this. This linear function of `n_sequences` I found it empirically.
        
        volts = np.array(raw_data).astype(float)
        volts[volts>127] -= 255
        volts[volts>127-1] = float('NaN') # This means that (very likely) there was overflow towards positive voltages.
        volts[volts<128-255+1] = float('NaN') # This means that (very likely) there was overflow towards negative voltages.
        volts = volts/25*self.get_vdiv(channel)-float(self.query(f'C{channel}:ofst?'))
        
        number_of_samples_per_waveform = int(self.query("VBS? 'return=app.Acquisition.Horizontal.NumPoints'")) # See https://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf p. 1-20.
        if sequence_status == 'ON':
            number_of_samples_per_waveform += 2 # Don't ask... Without this it fails. I discovered this by try and failure.
            volts = [volts[n_waveform*number_of_samples_per_waveform:(n_waveform+1)*number_of_samples_per_waveform] for n_waveform in range(n_segments_acquired)]
        else:
            volts = [volts]
            
        #print(len(volts))
        tdiv = float(self.query('TDIV?'))
        sampling_rate = float(self.query("VBS? 'return=app.Acquisition.Horizontal.SamplingRate'")) # This line is a combination of http://cdn.teledynelecroy.com/files/manuals/maui-remote-control-and-automation-manual.pdf and p. 1-20 http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf
        times = np.arange(len(volts[0]))/sampling_rate + tdiv*14/2 # See page 223 in http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf
        
        if sequence_status == 'OFF':
            return {'Time (s)': times, 'Amplitude (V)': volts[0]}
        else:
            return [{'Time (s)': times, 'Amplitude (V)': v} for v in volts]
    
    def get_triggers_times(self, channel: int)->list:
        """Gets the trigger times (with respect to the first trigger). What
        this function returns is the list of numbers you find if you go
        in the oscilloscope window to "Timebase→Sequence→Show Sequence Trigger Times...→since Segment 1"
        
        Arguments
        ---------
        channel: int
            Number of channel from which to get the data.
        
        Returns
        -------
        trigger_times: list
            A list of trigger times in seconds from the first trigger.
        """
        _validate_channel_number(channel)
        raw = self.query(f"VBS? 'return=app.Acquisition.Channels(\"C{channel}\").TriggerTimeFromRef'") # To know this command I used the `XStream Browser` app in the oscilloscope's desktop.
        raw = [int(i) for i in raw.split(',') if i != '']
        datetimes = [datetime.datetime.fromtimestamp(i/1e10) for i in raw] # Don't know why we have to divide by 1e10, but it works...
        datetimes = [i-datetimes[0] for i in datetimes]
        return [i.total_seconds() for i in datetimes]
    
    def wait_for_single_trigger(self,timeout=-1):
        """Sets the trigger in 'SINGLE' and blocks the execution of the
        program until the oscilloscope triggers.
        - timeout: float, number of seconds to wait until rising a 
        RuntimeError exception. If timeout=-1 it is infinite."""
        try:
            timeout = float(timeout)
        except:
            raise TypeError(f'<timeout> must be a float number, received object of type {type(timeout)}.')
        self.set_trig_mode('SINGLE')
        start = time.time()
        while self.query('TRIG_MODE?') != 'STOP':
            time.sleep(.1)
            if timeout >= 0 and time.time() - start > timeout:
                raise RuntimeError(f'Timed out waiting for oscilloscope to trigger after {timeout} seconds.')
    
    def Trigger(self, mode: str):
        """Triggers the WF mode."""
        self.write('TRIG_MODE ' + mode)
        
    def set_trig_mode(self, mode: str):
        """Sets the trigger mode."""
        OPTIONS = ['AUTO', 'NORM', 'STOP', 'SINGLE']
        if mode.upper() not in OPTIONS:
            raise ValueError('<mode> must be one of ' + str(OPTIONS))
        self.write('TRIG_MODE ' + mode)
    
    def set_vdiv(self, channel: int, vdiv: float):
        """Sets the vertical scale for the specified channel."""
        try:
            vdiv = float(vdiv)
        except:
            raise TypeError(f'<vdiv> must be a float number, received object of type {type(vdiv)}.')
        _validate_channel_number(channel)
        self.write(f'C{channel}:VDIV {float(vdiv)}') # http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=47
    
    def set_tdiv(self, tdiv: str):
        _validate_t_div_value(tdiv)
        """Sets the horizontal scale per division for the main window."""
        # See http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=151
        self.write(f'TDIV {tdiv}')

    def get_vdiv(self, channel: int):
        """Gets the vertical scale of the specified channel. Returns a 
        float number with the volts/div value."""
        _validate_channel_number(channel)
        return float(self.query(f'C{channel}:VDIV?')) # http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=47
    
    def set_trig_type(self, type: str):
        """Sets the trigger type as a string."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=40
        _validate_trig_type(type)
        string = "VBS 'app.Acquisition.Trigger.Type = "
        string += '"' + type + '"'
        string += "'"
        self.write(string)
    
    def get_trig_source(self):
        """Returns the trigger source as a string."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=34
        return str(self.query("VBS? 'return=app.Acquisition.Trigger.Source'"))
    
    def set_trig_source(self, source: str):
        """Sets the trigger source (C1, C2, Ext, etc.)."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=34
        _validate_trig_source(source)
        string = "VBS 'app.Acquisition.Trigger.Source = "
        string += '"' + source + '"'
        string += "'"
        self.write(string)
    
    def set_trig_coupling(self, trig_source: str, trig_coupling: str):
        """Set the trigger coupling (DC, AC, etc.)."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=37
        _validate_trig_source(trig_source)
        VALID_TRIG_COUPLINGS = {'AC','DC','HFREJ','LFREJ'}
        if not isinstance(trig_coupling, str) or trig_coupling.lower() not in {tc.lower() for tc in VALID_TRIG_COUPLINGS}:
            raise ValueError(f'The trigger coupling must be one of {VALID_TRIG_COUPLINGS}, received {repr(trig_coupling)}...')
        string = f"VBS 'app.Acquisition.Trigger.{trig_source}.Coupling = "
        string += '"' + trig_coupling + '"'
        string += "'"
        self.write(string)
    
    def set_trig_level(self, trig_source: str, level: float):
        """Set the trigger level."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=36
        _validate_trig_source(trig_source)
        if not isinstance(level, (float, int)):
            raise ValueError(f'The trigger level must be a float number, received object of type {type(level)}.')
        string = f"VBS 'app.Acquisition.Trigger.{trig_source}.Level = "
        string += '"' + str(level) + '"'
        string += "'"
        self.write(string)
    
    def set_trig_slope(self, trig_source: str, trig_slope: str):
        """Set the trigger slope (Positive, negative, either)."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=36
        _validate_trig_source(trig_source)
        VALID_TRIG_SLOPES = {'Positive', 'Negative', 'Either'}
        if not isinstance(trig_slope, str) or trig_slope.lower() not in {tslp.lower() for tslp in VALID_TRIG_SLOPES}:
            raise ValueError(f'The trigger coupling must be one of {VALID_TRIG_SLOPES}, received {repr(trig_slope)}...')
        string = f"VBS 'app.Acquisition.Trigger.{trig_source}.Slope = "
        string += '"' + trig_slope + '"'
        string += "'"
        self.write(string)
    
    def set_trig_delay(self, trig_delay: float):
        """Set the trig delay, i.e. the time interval between the trigger event and the center of the screen."""
        # See http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=152
        if not isinstance(trig_delay, (float, int)):
            raise ValueError(f'The trigger delay must be a number, received object of type {type(trig_delay)}.')
        self.write(f'TRIG_DELAY {trig_delay}')
    
    def sampling_mode_sequence(self, status:str, number_of_segments:int=None)->None:
        """Configure the "sampling mode sequence" in the oscilloscope. See
        [here](https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-automation_27jul22.pdf#%5B%7B%22num%22%3A1235%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C54%2C743.25%2C0%5D).
        
        Arguments
        ---------
        status: str
            Either 'on' or 'off'.
        number_of_segments: int
            Number of segments, i.e. number of "sub triggers" within the
            sequence mode.
        """
        if not isinstance(status, str) or status.lower() not in {'on','off'}:
            raise ValueError(f'`status` must be a string, either "on" or "off", received {status} of type {type(status)}.')
        if number_of_segments is not None and not isinstance(number_of_segments, int):
            raise TypeError(f'`number_of_segments` must be an integer number.')
        cmd = f'SEQUENCE {status.upper()}'
        if number_of_segments is not None:
            cmd += f',{number_of_segments}'
        self.write(cmd)
    
    def set_sequence_timeout(self, sequence_timeout:float, enable_sequence_timeout:bool=True):
        """Configures the "Sequence timeout" in the oscilloscope both value
        and enable/disable.
        
        Arguments
        ---------
        sequence_timeout: float
            Timeout value in seconds.
        enable_sequence_timeout: bool, default `True`
            Enable or disable the sequence timeout functionality.
        """
        if not isinstance(sequence_timeout, (int,float)):
            raise TypeError(f'`sequence_timeout` must be a float number, received object of type {type(sequence_timeout)}.')
        if not enable_sequence_timeout in {True, False}:
            raise TypeError(f'`enable_sequence_timeout` must be a boolean, received object of type {type(enable_sequence_timeout)}.')
        enable_sequence_timeout = 'true' if enable_sequence_timeout==True else 'false'
        self.write(f"VBS 'app.Acquisition.Horizontal.SequenceTimeout = {sequence_timeout}'")
        self.write(f"VBS 'app.Acquisition.Horizontal.SequenceTimeoutEnable = {enable_sequence_timeout}'")

    def set_trace(self, trig_source: str, status: str):
        """Set the channel trace to ON/OFF."""
        # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=29
        _validate_trig_source(trig_source)
        string = f"VBS 'app.Acquisition.{trig_source}.View = "
        if status == "ON":
            string += '"' + True + '"'
        else:
            string += '"' + False + '"'
        string += "'"
        self.write(string)
    
    def set_units_per_volt(self, channel: int, value: float):
        """Sets the vertical scale for the specified channel."""
        try:
            value = float(value)
        except:
            raise TypeError(f'<value> must be a float number, received object of type {type(value)}.')
        _validate_channel_number(channel)
        self.write(f"vbs? 'app.Acquisition.C{channel}.Multiplier = {float(value)}'") 
         # See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=348

    def save_parameters_trace(self, path:str, channel: int, fileformat:str, id:str):
        _validate_waveform_format(fileformat)
        """measure the parameters of the trace for the specified channel."""
        _validate_channel_number(channel)
        pkpk = self.query(f"C{channel}:PAVA? PKPK")
        ampl = self.query(f"C{channel}:PAVA? AMPL")
        max = self.query(f"C{channel}:PAVA? MAX")
        min =self.query(f"C{channel}:PAVA? MIN")
        sdev = self.query(f"C{channel}:PAVA? SDEV")
        mean = self.query(f"C{channel}:PAVA? MEAN")
        base = self.query(f"C{channel}:PAVA? BASE")
        top = self.query(f"C{channel}:PAVA? TOP")
        # See http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=101
        parameters = [pkpk, ampl, max, min, sdev, mean, base, top]

        print("Saving measured parameters...")
        #dir = self.query("vbs? 'app.SaveRecall.Waveform.WaveformDir '")
        # create a new XLSX workbook
        wb = xlsxwriter.Workbook(fr"{path}\{id}.xlsx")
        worksheet = wb.add_worksheet()
        # insert value in the cells
        for row_num, data in enumerate(parameters):
            worksheet.write(row_num, 0, data)

        wb.close()
        print("Parameters saved successfully!")

        return parameters

    def save_waveform_on_OSC(self, fileformat:str, channel:int, filename:str):
        print("Saving waveform data on OSC....")
        self.write(f"vbs 'app.SaveRecall.Waveform.WaveFormat = \"{fileformat}\" '")
        self.write(f"vbs 'app.SaveRecall.Waveform.SaveSource = \"C{channel}\" '")
        self.query("vbs? 'app.SaveRecall.Waveform.SaveFile'")
        self.query("vbs? 'app.SaveRecall.Waveform.EnableCounterSuffix = false'")
        self.query("vbs? 'app.SaveRecall.Waveform.EnableSourcePrefix = false'")
        self.query(f"vbs? 'app.SaveRecall.Waveform.TraceTitle = \"{filename}\" '")
        #self.query("vbs? 'app.SaveRecall.Utilities.Directory")                      
        self.query("vbs? 'app.SaveRecall.Utilities.Directory'")
        print("Waveform data saved successfully on Oscilloscope!")
    
    def get_waveform_from_osc(self, id:str):        # %%% CHECK 
        osc_path = self.read("vbs?' app.SaveRecall.Utilities.DestDirectory'")
        print(osc_path)
        #self.write("vbs' app.SaveRecall.Utilities.DestDirectory'")
       #file_path = r"C:\Users\DAV1SI\Desktop\test"
       #os.path.join(osc_path, id)
        print("FIle saved successfuly on PC")
            
        
    def save_waveform_on_PC(self, path:str, waveform:pd.DataFrame, id:str): #CHECK
        if not os.path.exists(path):
            os.makedirs(path)
        id = id + ".csv"
        print("Saving waveform data in excel on controlling PC....")
        waveform.to_csv(os.path.join(path,id))
        print("Waveform data saved successfully on controlling PC!")
        
        
# if __name__ == "__main__":
#     osc =osc = Oscilloscope("TCPIP0::192.168.40.26::inst0::INSTR")
#     osc.query("VBS?'app.SaveRecall.Waveform.RecallFilename'")
        
