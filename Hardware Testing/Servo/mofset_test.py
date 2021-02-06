import RPi.GPIO as GPIO
import time

pin = 40

GPIO.setmode(GPIO.BOARD) # Board Numbering Scheme
GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, GPIO.HIGH)
print('On')
time.sleep(10)

GPIO.output(pin, GPIO.LOW)
print('Off')

GPIO.cleanup()
