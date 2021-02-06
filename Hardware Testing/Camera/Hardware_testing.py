import time
import picamera
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
    time.sleep(2)
        
    print ("LED on")
    for pins in pin_nums:
        GPIO.output(pins,GPIO.HIGH)
    
    time.sleep(1)
    camera.capture('foo.jpg')
    print(" Capture Complete")
    time.sleep(1)
    for pins in pin_nums:
        GPIO.output(pins,GPIO.LOW)
        
    print("LED off")