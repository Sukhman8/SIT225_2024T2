import serial  
import time  
import random 
# Establish a serial connection with Arduino on COM8 at a baud rate of 9600
# 'timeout=1' ensures that readline() does not block indefinitely
arduino = serial.Serial('COM8', 9600, timeout=1)

def send_command():
    """Send a random number to Arduino and log the event."""
    blink_count = random.randint(1, 5)  # Generate a random number between 1 and 5
    arduino.write(f"{blink_count}\n".encode())  # Send the number as a string, encoded in bytes
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] → Sent to Arduino: {blink_count}")
    return blink_count  # Return the number sent for reference

def wait_for_response():
    """Listen for Arduino's response and wait accordingly."""
    while True:  
        if arduino.in_waiting > 0:  # Check if there is incoming data from Arduino
            try:
                response = arduino.readline().decode().strip()  # Read and decode the response
                wait_time = int(response)  # Convert the response to an integer
                
                # Log the received random number
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ← Received from Arduino: {wait_time}")
                
                # Pause execution for the received time (simulating a delay)
                time.sleep(wait_time)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  Paused for {wait_time} seconds.")
                break  # Exit the loop after processing a valid response
            
            except ValueError:
                # Handle the case where the response is not a valid integer
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  Invalid response, retrying...")

def start_communication():
    """Continuously send and receive data between Python and Arduino."""
    while True:
        send_command()  # Send a random number to Arduino
        time.sleep(0.2)  # Short delay before listening for a response
        wait_for_response()  # Wait for Arduino’s response and pause accordingly

# Run the communication process when the script is executed
if __name__ == "__main__":
    start_communication()

