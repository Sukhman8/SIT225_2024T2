
import csv
import time
from datetime import datetime
import serial

# Arduino Serial Port Configuration
SERIAL_PORT = "COM8"  # Change to your Arduino's port
BAUD_RATE = 9600
CSV_FILE = "accelerometer_data.csv"
VARIABLES = ["accelX", "accelY", "accelZ"]

# Open Serial Connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def save_to_csv(data):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["timestamp"] + VARIABLES)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + data)

def main():
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    parts = line.split()
                    if len(parts) == 6:  # Ensuring correct format
                        accelX, accelY, accelZ = map(float, [parts[1], parts[3], parts[5]])
                        save_to_csv([accelX, accelY, accelZ])
                        print(f"Saved: X={accelX}, Y={accelY}, Z={accelZ}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping data collection.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()