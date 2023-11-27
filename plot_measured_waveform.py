import pandas as pd
import matplotlib.pyplot as plt

# Read data from saved Excel file
df = pd.read_csv(fr"C:\Users\DAV1SI\Desktop\test\C1_23_NOV_2023_16_45_17.csv")
# print(f"Column names C{str(i)}:", df.columns)

# Extract Time and Amplitude columns


# Plot the data
plt.plot(df['Time (s);Amplitude (V)'])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.title('Acquired Waveform')
plt.grid(True)
plt.show()
