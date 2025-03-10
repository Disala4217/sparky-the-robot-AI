import cv2
import RPi.GPIO as GPIO
from time import sleep

# Define GPIO pins
ypin = 11
xpin = 13

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(xpin, GPIO.OUT)
GPIO.setup(ypin, GPIO.OUT)

x = GPIO.PWM(xpin, 50)
y = GPIO.PWM(ypin, 50)

# Define the servopos class
class servopos():
    def __init__(self):
        self.currentx, self.currenty = 7, 4
        x.start(self.currentx)
        y.start(self.currenty)
        sleep(1)
        x.ChangeDutyCycle(0)
        y.ChangeDutyCycle(0)

    def setposx(self, diffx):
        self.currentx += diffx
        self.currentx = round(self.currentx, 2)
        if 0 < self.currentx < 15:
            x.ChangeDutyCycle(self.currentx)
            sleep(0.02)
            x.ChangeDutyCycle(0)

    def setposy(self, diffy):
        self.currenty += diffy
        self.currenty = round(self.currenty, 2)
        if 0 < self.currenty < 15:
            y.ChangeDutyCycle(self.currenty)
            sleep(0.02)
            y.ChangeDutyCycle(0)

    def setdcx(self, dcx):
        x.ChangeDutyCycle(dcx)

    def setdcy(self, dcy):
        y.ChangeDutyCycle(dcy)

# Initialize the servo object
ser = servopos()

# Load the face cascade
cascade_path = '/home/disala/Desktop/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# PID coefficients
Px, Ix, Dx = -1/160, 0, 0
Py, Iy, Dy = -0.2/120, 0, 0

# Initialize other required variables
integral_x, integral_y = 0, 0
differential_x, differential_y = 0, 0
prev_x, prev_y = 0, 0
width, height = 320, 240

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Allow the camera to warm up
sleep(0.1)

# Define the function face_detected() to be called when a face is detected
def face_detected():
    print("Face detected!")

# Capture frames from the camera
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    frame = cv2.flip(frame, 1)
    
    ser.setdcx(0)
    ser.setdcy(0)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect face coordinates x, y, w, h
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    c = 0
    for (fx, fy, fw, fh) in faces:
        c += 1
        if c > 1:  # We just take care of the first face detected
            break
        
        # Centre of face
        face_centre_x = fx + fw / 2
        face_centre_y = fy + fh / 2
        
        # Calculate pixels to move
        error_x = 160 - face_centre_x  # X-coordinate of Centre of frame is 160
        error_y = 120 - face_centre_y  # Y-coordinate of Centre of frame is 120
        
        integral_x += error_x
        integral_y += error_y
        
        differential_x = prev_x - error_x
        differential_y = prev_y - error_y
        
        prev_x = error_x
        prev_y = error_y
        
        valx = Px * error_x + Dx * differential_x + Ix * integral_x
        valy = Py * error_y + Dy * differential_y + Iy * integral_y
        
        valx = round(valx, 2)  # Round off to 2 decimal points
        valy = round(valy, 2)
        
        if abs(error_x) < 20:
            ser.setdcx(0)
        else:
            if abs(valx) > 0.5:
                sign = valx / abs(valx)
                valx = 0.5 * sign
            ser.setposx(valx)
        
        if abs(error_y) < 20:
            ser.setdcy(0)
        else:
            if abs(valy) > 0.5:
                sign = valy / abs(valy)
                valy = 0.5 * sign
            ser.setposy(valy)
        
        frame = cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 6)
        
        # Call the function when a face is detected
        face_detected()
    
    # Display the frame
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
