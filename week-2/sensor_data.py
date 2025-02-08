import serial
import time
import csv

SERIAL_PORT = "COM8"  
BAUD_RATE = 9600
FILENAME = "distance_data.csv"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  

print("Collecting HC-SR04 distance data... Press Ctrl+C to stop.")

try:
    
    with open(FILENAME, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Timestamp", "Distance (cm)"])  

        while True:
            if ser.in_waiting > 0:
                try:
                    distance = ser.readline().decode().strip() 

                    
                    if distance and distance.replace('.', '', 1).isdigit():
                        timestamp = time.strftime('%Y%m%d%H%M%S')  
                        print(f"{timestamp}, {distance}")  

                       
                        csv_writer.writerow([timestamp, distance])
                        file.flush()  

                except Exception as e:
                    print(f"Error reading data: {e}")  

            time.sleep(1)  

except KeyboardInterrupt:
    print("\nData collection stopped. CSV file saved.")
    ser.close()
