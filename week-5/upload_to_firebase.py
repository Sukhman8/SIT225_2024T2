import serial
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")  
firebase_admin.initialize_app(cred, {"databaseURL": "https://dct5-1c-default-rtdb.firebaseio.com/"}) 
ser = serial.Serial("COM8", 115200)  

while True:
    try:
        data = ser.readline().decode("utf-8").strip()
        timestamp, x, y, z = data.split(",")

        # Prepare JSON
        gyro_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "x": float(x),
            "y": float(y),
            "z": float(z),
        }

        # Upload to Firebase
        db.reference("gyroscope_data").push(gyro_data)
        print("Uploaded:", gyro_data)

    except Exception as e:
        print("Error:", e)
        break
