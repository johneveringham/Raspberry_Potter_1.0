import picamera     # Importing the library for camera module
from time import sleep  # Importing sleep from time library to add delay in program

time_record = 25; # seconds
save_location = r'/home/pi/Desktop/video.h264';

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin_nums = [14,15,18,23]

for pins in pin_nums:
    GPIO.setup(pins,GPIO.OUT)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
        
    print ("LEDs on")
    for pins in pin_nums:
        GPIO.output(pins,GPIO.HIGH)
    sleep(0.5)
    
    camera.start_preview()      # You will see a preview window while recording
    camera.start_recording(save_location) # Video will be saved at desktop
    sleep(time_record)
    camera.stop_recording()
    camera.stop_preview()

    print(" Capture Complete")
    sleep(1)
    for pins in pin_nums:
        GPIO.output(pins,GPIO.LOW)
        
    print("LEDs off")