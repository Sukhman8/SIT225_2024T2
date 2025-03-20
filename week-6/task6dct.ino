#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("timestamp,gyro_x,gyro_y,gyro_z");  // CSV Header
}

void loop() {
  float x, y, z;
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
    
    // Print gyroscope data in CSV format
    Serial.print(millis()); Serial.print(",");
    Serial.print(x); Serial.print(",");
    Serial.print(y); Serial.print(",");
    Serial.println(z);
  }
  delay(100); // Collect data every 100ms
}
