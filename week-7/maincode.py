import serial
import time
import csv

# Open serial port (Update the COM port as per your system)
ser = serial.Serial('COM8', 9600)  
time.sleep(2)  # Wait for Arduino to initialize

# Open CSV file and set up header
with open('sensor_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Temperature (°C)", "Humidity (%)"])

    try:
        while True:
            data = ser.readline().decode().strip()
            print(data)

            # Match line like: "Temperature: 24.0 °C    Humidity: 52.0 %"
            if data.startswith("Temperature:") and "Humidity:" in data:
                try:
                    temp_part = data.split("Temperature:")[1].split("°C")[0].strip()
                    hum_part = data.split("Humidity:")[1].split("%")[0].strip()

                    temperature = float(temp_part)
                    humidity = float(hum_part)

                    # Write to CSV with current time
                    writer.writerow([time.strftime("%H:%M:%S"), temperature, humidity])

                except ValueError:
                    print("Data parsing error.")

    except KeyboardInterrupt:
        print("Data logging stopped by user.")
