#include <Arduino_LSM6DS3.h>
#include "thingProperties.h"
// Variables to store accelerometer data
float accelX, accelY, accelZ;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize the IMU (accelerometer)
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  // Read accelerometer data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accelX, accelY, accelZ);
    
    // Print data to Serial Monitor for debugging
    Serial.print("X: ");
    Serial.print(accelX);
    Serial.print(" Y: ");
    Serial.print(accelY);
    Serial.print(" Z: ");
    Serial.println(accelZ);
    
    // Update Arduino Cloud variables
    // Note: Replace with your actual Arduino Cloud variable update functions
    // cloud.updateVariable("accelX", accelX);
    // cloud.updateVariable("accelY", accelY);
    // cloud.updateVariable("accelZ", accelZ);
  }
  
  // Delay for a short period
  delay(100);
}