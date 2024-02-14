**LeCroy-Oscilloscope-Automation**

The purpose of this script is to automate and customize the setup and trigger functionalities of an Oscilloscope.

Oscilloscope_PyVisa.py has the Oscilloscope Class and various Oscilloscope Automation Commands as it's methods.

SET_TRIGGER_SEQ.py defines the SET_SINGLE_TRIGGER & SET_NORMAL_TRIGGER functions.

TRIGGER_SEQ.py has all the configurable Channel, Timebase and Trigger parameters to trigger the OSC in SINGLE or NORMAL mode and save the triggered waveforms & it's parameters on the controlling PC.

plot_measured_Waveform.py helps in validating the saved waveforms.

------------------------------------------------------------------------------------------------------------------------------------------
**OSCILLOSCOPE SETUP INSTRUCTIONS:**

i. Make sure Firewall is Disabled on BOTH the OSC and PC

ii. REMEMBER to set the correct IP of OSC and select the LXI(VXI1) protocol from "Utilities-> Utilities Setup-> Remote-> Control From" in DSO application on OSC. Make sure OSC and PC have the same subnet

iii. Check if OSC can be pinged via Command Prompt with: ping "ip_address" 

iv. If you cannot connect ping to OSC,

a. check IP address and IP subnet of OSC & PC
b. Turn Firewall OFF on OSC
c. select remote protocol as LXI
d. check resource string in osc.connect attribute in Oscilloscope_PyVisa.py (change VICP to TICP0 and vice-versa and check if it works. !! Works sometimes)
e. Check if ActiveDSO or VICP Passport is installed on controlling PC. (if not, both can be installed from LeCroy website) 

------------------------------------------------------------------------------------------------------------------------------------------

**You need the "TRIGGER_SEQ.py" script to Trigger the OSC in SINGLE or NORMAL mode**

**Note: To run the script, you only need to change the Config parameters at the top of the script as per your requirement.**

1. Set the individual channel Vertical & Horizontal settings using the "SET_CHANNEL_PARAMETERS" & "timebase_settings" attributes of Oscilloscope Library and save the setup file as a "File" or in oscilloscope "Memory" with your specific name/date in a specific folder.

2. You can use the same setup the next time you want to use the OSC by recalling this saved setup file via "recall_setup" function.

!Comment out the save and recall setup commands when not needed

3. Use "SET_SINGLE_TRIGGER" or "SET_NORMAL_TRIGGER" function as per your requirement and specify the respective Trigger Parameters as entioned in the file.

4. Specify the correct paths to save the file on OSC and controlling PC. Also, you can use retrieve_waveform function to get waveforms with specific ID's and store them in another folder of your choice with the same folder name as the Trigger ID.

5. Run the code and use "plot_measured_waveform.py" with the name of the waveform .csv/.txt file to validate the saved signal.