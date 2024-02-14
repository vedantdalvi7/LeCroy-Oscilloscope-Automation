import pandas as pd
import matplotlib.pyplot as plt

'''THIS SCRIPT HELPS TO PLOT THE SAVED WAVEFORM ON CONTROLLING PC TO VERIFY/VALIDATE'''

file_path = r"C:\Users\DAV1SI\Desktop\test"                              #SPECIFIY FILEPATH OF WAVEFORM .CSV OR .TXT FILE
filename = "C1_12_FEB_2024_13_54_49_waveform.csv"                        #SPECIFIY FILENAME OF WAVEFORM .CSV OR .TXT FILE

if ".csv" in filename:

    # Read data from saved Excel file
    df = pd.read_csv(fr"{file_path}/{filename}")

    # Plot the data
    plt.plot(df)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.title(f'Saved Waveform: {filename.split(".")[0]}')
    plt.grid(True)
    plt.show()

elif ".txt" in filename:
    time = [] 
    amplitude = [] 
    
    f = open(file_path+"/"+filename,'r') 
    for row in f: 
        row = row.split(',') 
        time.append(row[0]) 
        amplitude.append(float(row[1])) 
    
    plt.bar(time, amplitude, color = 'g', label = 'File Data') 
    
    plt.xlabel('time', fontsize = 12) 
    plt.ylabel('amplitude', fontsize = 12) 
    
    plt.title('Saved Waveform', fontsize = 20) 
    plt.grid(True)
    plt.legend() 
    plt.show() 

    # # Load data from text file
    # data = np.loadtxt(file_path)

    # # Separate data into x and y columns
    # x = data[:, 0]
    # y = data[:, 1]

    # # Plot the data
    # plt.plot(x, y)
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude (V)')
    # plt.title(f'Saved Waveform: {file_path.split(".")[0]}')
    # plt.grid(True)
    # plt.show()

else:
    print(".csv or .txt file not found! Please specify correct file format!")