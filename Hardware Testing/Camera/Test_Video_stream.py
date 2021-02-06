# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin_nums = [14,15,18,23]

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image - this array
    # will be 3D, representing the width, height, and # of channels
    image = frame.array
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
#
#for pins in pin_nums:
#    GPIO.setup(pins,GPIO.OUT)
#
#with picamera.PiCamera() as camera:
#    camera.resolution = (640, 480)
#    camera.start_preview()
#    # Camera warm-up time
#    time.sleep(2)
#        
#    print ("LED on")
#    for pins in pin_nums:
#        GPIO.output(pins,GPIO.HIGH)
#    
#    time.sleep(1)
#    camera.capture('foo.jpg')
#    print(" Capture Complete")
#    time.sleep(1)
#    for pins in pin_nums:
#        GPIO.output(pins,GPIO.LOW)
#        
#    print("LED off")