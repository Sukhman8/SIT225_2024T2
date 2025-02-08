import pandas as pd
import matplotlib.pyplot as plt

filename = "Sumit.csv"
df = pd.read_csv(filename)

print(df.head())

df = df[df['Time'].astype(str).str.isnumeric()]

df['Timestamp'] = pd.to_datetime(df['Time'], format="%Y%m%d%H%M%S", errors='coerce')

df = df.dropna(subset=['Timestamp'])
df['Distance in (cm)'] = df['Distance in (cm)'].astype(str).str.extract(r'(\d+)').astype(float)

df['Smoothed_Distance'] = df['Distance in (cm)'].rolling(window=5, min_periods=1).mean()

plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Smoothed_Distance'], marker='o', markersize=1, linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Distance (cm)')
plt.title('Ultrasonic Sensor Readings (Smoothed)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()