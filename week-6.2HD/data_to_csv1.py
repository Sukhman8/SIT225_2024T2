import serial
import csv
import time

ser = serial.Serial('COM8', 115200, timeout=1)
time.sleep(2)  # Wait for connection

# Open CSV file
with open("gyroscope_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time(ms)", "X", "Y", "Z"])  # Header
    
    while True:
        line = ser.readline().decode("utf-8").strip()
        if line and not line.startswith("Gyroscope"):  
            writer.writerow(line.split(", "))
            print(line)
