#define TRIG_PIN 9  // Trigger Pin of HC-SR04
#define ECHO_PIN 10 // Echo Pin of HC-SR04

void setup() {
    Serial.begin(9600);  
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
    long duration;
    float distance;

    // Send trigger signal
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    // Read echo signal
    duration = pulseIn(ECHO_PIN, HIGH);
    
    // Convert time to distance (cm)
    distance = duration * 0.034 / 2;

    // Send distance value to Serial (for Python)
    Serial.println(distance);

    delay(1000);  // Sample every second
}
