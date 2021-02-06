import RPi.GPIO as GPIO
import time

def change_angle(angle, servo):
    duty = float(angle)/18.0 + 2.5
    servo.ChangeDutyCycle(duty)

def open_close(t):
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    servo = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    servo.start(0) # Initialization

    change_angle(0,servo)
    time.sleep(t)

    change_angle(180,servo)
    time.sleep(t)

    servo.stop()
    GPIO.cleanup()

open_close(5)

