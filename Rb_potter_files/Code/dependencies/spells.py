import RPi.GPIO as GPIO
import time
import board
import neopixel
import pygame

#Testing Fuctions
#==============================
def test_all():
    pixels = setup_neo_pix()

    luomos_max(pixels)
    time.sleep(1)
    luomos_max(pixels)
    
#     leviosa()
#     play_sound('harry_potter_loop (4).mp3') 
    
#Spells
#==============================
def leviosa():
    play_sound('itsleviosa_HEW2LBa (3).mp3')
    
def setup_neo_pix():
    # Set GPIO Mode for neopixel
    GPIO.setmode(GPIO.BCM)
    
    # Setup Neopixel
    pixel_pin = board.D21

    # The number of NeoPixels
    num_pixels = 16

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )
    
    return pixels
   
def test_neo_pix(pixels):
    # Lights
    slow_bright(pixels, color = (120,120,95), t = 2,dt = .2)
    off(pixels)

def alohomora(pixels):
    #Action
    open_box()
    
    # Sound
    play_sound('harry_potter_loop (4).mp3')
    
    # Lights
    slow_bright(pixels, color = (0,90,120), t = 8,dt = .2)
    cycle_purple(0.001, pixels, t = 11)
    off(pixels)

    #Action
    close_box()

def luomos_max(pixels):
    
    #Action
    open_box(angle = 90)
    
    # Sound
    play_sound('Lumos Maxima  HP (2).mp3')
    
    # Lights
    slow_bright(pixels, color = (120,120,95), t = 15,dt = .2)
    off(pixels)
    
    #Action
    close_box()

#Sounds
#==============================
def play_sound(filename):
    path = '/home/pi/Desktop/Raspberry_Potter/Rb_potter_files/Sounds'
    filepath = path + '//' + filename

    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

#Servo
#==============================
def change_angle(angle, servo):
    duty = float(angle)/18.0 + 2.5
    servo.ChangeDutyCycle(duty)
   
def open_box(angle = 0):
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    servo = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    servo.start(0) # Initialization

    change_angle(angle ,servo)
    time.sleep(3)
    
    servo.stop()
    GPIO.cleanup()
    time.sleep(3)
    
def close_box():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    servo = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    servo.start(0) # Initialization
    
    change_angle(180,servo)
    time.sleep(3)

    servo.stop()
    GPIO.cleanup()
    time.sleep(3)
    
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
    
#NeoPixel
#==============================   
def slow_bright(pixels, color = (0,100,0), t = 20, dt = 0.4):
    r = color[0]
    g = color[1]
    b = color[2]
    
    steps = int(t/dt)
    if steps > max(color):
        steps = max(color)
        
    r_step = int(r/steps)
    g_step = int(g/steps)
    b_step = int(b/steps)
    
    r = 0
    g = 0
    b = 0
    
    for i in range(steps):
        r += r_step
        g += g_step
        b += b_step
        
        pixels.fill((g,r,b))
        pixels.show()
        time.sleep(dt)
        
def wheel_purple(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = 0
        b = int(pos * 3)
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(255 - pos * 3)
    else:
        pos -= 170
        r = int(255 - pos * 3)
        g = 0
        b = int(255 - pos * 3)
        
        r = int(r*0.4)
    return (r, g, b)
            
def cycle_purple(wait, pixels, t = 5):
    duration = 0
    num_pixels = len(pixels)
    
    while duration < t:
        start = time.time()
        
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel_purple(pixel_index & 255)
                
            pixels.show()
            time.sleep(wait)
            stop = time.time()
            duration += ((stop-start)/100)

def off(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(3)

# if __name__ == "__main__":
#     test_all()