import RPi.GPIO as GPIO
from time import sleep

# Define GPIO pins
xpin = 11  # GPIO pin for X-axis servo
ypin = 13  # GPIO pin for Y-axis servo

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(xpin, GPIO.OUT)
GPIO.setup(ypin, GPIO.OUT)

# Initialize PWM on the pins at 50Hz
x = GPIO.PWM(xpin, 50)
y = GPIO.PWM(ypin, 50)

# Function to test the servo positions
def test_servos():
    # Start PWM with a duty cycle of 0 (stop pulse)
    x.start(0)
    y.start(0)
    
    try:
        while True:
            # Move servos to 0 degrees
            print("Moving to 0 degrees")
            x.ChangeDutyCycle(2.5)  # 0 degrees
            y.ChangeDutyCycle(2.5)  # 0 degrees
            sleep(1)
            
            # Move servos to 90 degrees
            print("Moving to 90 degrees")
            x.ChangeDutyCycle(7.5)  # 90 degrees
            y.ChangeDutyCycle(7.5)  # 90 degrees
            sleep(1)
            
            # Move servos to 180 degrees
            print("Moving to 180 degrees")
            x.ChangeDutyCycle(12.5)  # 180 degrees
            y.ChangeDutyCycle(12.5)  # 180 degrees
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup the GPIO and stop PWM
        x.stop()
        y.stop()
        GPIO.cleanup()

# Run the test
test_servos()
