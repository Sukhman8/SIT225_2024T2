#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h>

// WiFi Credentials
const char* ssid = "Makkar's S23";         // Your WiFi SSID
const char* password = "makkar@123";     // Your WiFi Password

// MQTT Broker (HiveMQ Cloud)
const char* mqttServer = "9ee13c6e36f24d13b7aed1c23d643834.s1.eu.hivemq.cloud";
const int mqttPort = 8883; // Secure TLS port
const char* mqttUser = "sukhman";
const char* mqttPassword = "Makkar@123";
const char* sensorTopic = "sensor/gyroscope"; // MQTT Topic for publishing & subscribing

// Initialize WiFi and MQTT Clients
WiFiSSLClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
    Serial.begin(115200);
    while (!Serial);

    Serial.println("\n=== WiFi & MQTT Debugging ===");

    // Connect to WiFi
    connectWiFi();

    // Configure MQTT Server
    client.setServer(mqttServer, mqttPort);
    client.setCallback(callback);

    // Connect to MQTT Broker
    connectMQTT();

    // Initialize IMU sensor
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
}

void loop() {
    if (!client.connected()) {
        connectMQTT();
    }
    client.loop();

    float x, y, z;
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);

        String payload = "{\"sensor_name\":\"LSM6DS3\",\"timestamp\":" + String(millis()) +
                         ",\"x\":" + String(x) + ",\"y\":" + String(y) + ",\"z\":" + String(z) + "}";

        client.publish(sensorTopic, payload.c_str());
        Serial.println("Data sent to MQTT: " + payload);
    }

    delay(5000);
}

// Function to connect to WiFi
void connectWiFi() {
    Serial.print("Connecting to WiFi...");
    WiFi.begin(ssid, password);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
        attempts++;
        if (attempts > 15) {
            Serial.println("\nWiFi connection failed. Restarting...");
            WiFi.disconnect();
            delay(5000);
            WiFi.begin(ssid, password);
            attempts = 0;
        }
    }

    Serial.println("\nConnected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}

// Function to connect to MQTT Broker
void connectMQTT() {
    while (!client.connected()) {
        Serial.print("Connecting to MQTT...");
        if (client.connect("ArduinoNanoClient", mqttUser, mqttPassword)) {
            Serial.println("Connected to MQTT Broker!");
            client.subscribe(sensorTopic); // Subscribe to a topic
        } else {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" Retrying in 5 seconds...");
            delay(5000);
        }
    }
}

// Callback function when a message is received
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.print(topic);
    Serial.print(" | Message: ");

    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}
