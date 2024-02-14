import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''PLOT THE SAVED WAVEFORM ON CONTROLLING PC TO VERIFY/VALIDATE'''

filename = "C6_14_FEB_2024_10_36_43_waveform.csv"                   #PLEASE SPECIFIY FILENAME OF WAVEFORM CSV FILE

# Read data from saved Excel file
df = pd.read_csv(fr"C:\Users\DAV1SI\Desktop\test\{filename}")

# Plot the data
plt.plot(df)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.title(f'Saved Waveform: {filename.split(".")[0]}')
plt.grid(True)
plt.show()

# #specify path to .txt file
# file_path = r"C:\Users\DAV1SI\Desktop\test\C1_12_FEB_2024_13_54_49_waveform.txt"

# time = [] 
# amplitude = [] 
  
# f = open(file_path,'r') 
# for row in f: 
#     row = row.split(',') 
#     time.append(row[0]) 
#     amplitude.append(float(row[1])) 
  
# plt.bar(time, amplitude, color = 'g', label = 'File Data') 
  
# plt.xlabel('time', fontsize = 12) 
# plt.ylabel('amplitude', fontsize = 12) 
  
# plt.title('Saved Waveform', fontsize = 20) 
# plt.grid(True)
# plt.legend() 
# plt.show() 

# # # Load data from text file
# # data = np.loadtxt(file_path)

# # # Separate data into x and y columns
# # x = data[:, 0]
# # y = data[:, 1]

# # # Plot the data
# # plt.plot(x, y)
# # plt.xlabel('Time (s)')
# # plt.ylabel('Amplitude (V)')
# # plt.title(f'Saved Waveform: {file_path.split(".")[0]}')
# # plt.grid(True)
# # plt.show()