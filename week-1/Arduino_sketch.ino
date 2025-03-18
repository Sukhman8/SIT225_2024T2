void setup() {
    Serial.begin(9600);  // Initialize serial communication at a baud rate of 9600
    pinMode(LED_BUILTIN, OUTPUT);  // Set the built-in LED pin as an output
}

void loop() {
    if (Serial.available() > 0) {  // Check if there is incoming data in the serial buffer
        int num = Serial.parseInt();  // Read an integer from the serial input

        if (num > 0) {  // If the received number is greater than 0
            for (int i = 0; i < num; i++) {  // Repeat the blinking process 'num' times
                digitalWrite(LED_BUILTIN, HIGH); // Turn the LED on
                delay(1000);  // Wait for 1 second
                digitalWrite(LED_BUILTIN, LOW);  // Turn the LED off
                delay(1000);  // Wait for 1 second
            }

            int r = random(2, 6); // Generate a random number between 2 and 5 (upper limit is exclusive)
            Serial.println(r);  // Print the random number to the Serial Monitor
        }
        delay(100);  // Short delay before checking for new serial input
    }
}
