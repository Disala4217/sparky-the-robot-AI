import RPi.GPIO as GPIO
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Define GPIO pins for servos
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
    
    def setposy(self, diffy):
        self.currenty += diffy
        self.currenty = round(self.currenty, 2)
        if 0 < self.currenty < 15:
            y.ChangeDutyCycle(self.currenty)
    
    def setdcx(self, dcx):
        x.ChangeDutyCycle(dcx)
    
    def setdcy(self, dcy):
        y.ChangeDutyCycle(dcy)

# Initialize servo control
ser = servopos()

# Load the Haar cascade file for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Set PID values for X and Y axis
Px, Ix, Dx = -1/160, 0, 0
Py, Iy, Dy = -0.2/120, 0, 0

integral_x, integral_y = 0, 0
differential_x, differential_y = 0, 0
prev_x, prev_y = 0, 0

# Initialize the camera
width, height = 320, 240
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(width, height))
time.sleep(1)

# Main loop to read frames and track face
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    frame = cv2.flip(image, 1)
    ser.setdcx(0)
    ser.setdcy(0)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    c = 0
    for (x, y, w, h) in faces:
        c += 1
        if c > 1:
            break
        
        face_centre_x = x + w / 2
        face_centre_y = y + h / 2
        
        error_x = 160 - face_centre_x
        error_y = 120 - face_centre_y
        
        integral_x += error_x
        integral_y += error_y
        
        differential_x = prev_x - error_x
        differential_y = prev_y - error_y
        
        prev_x = error_x
        prev_y = error_y
        
        valx = Px * error_x + Dx * differential_x + Ix * integral_x
        valy = Py * error_y + Dy * differential_y + Iy * integral_y
        
        valx = round(valx, 2)
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
        
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
GPIO.cleanup()
