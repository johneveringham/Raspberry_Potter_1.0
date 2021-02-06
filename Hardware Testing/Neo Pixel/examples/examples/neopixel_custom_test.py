# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
# pixel_pin = board.D21
# 
# # The number of NeoPixels
# num_pixels = 16
# 
# # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
# ORDER = neopixel.GRB
# 
# pixels = neopixel.NeoPixel(
#     pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
# )

def setup_neopixel(b = 0.2):
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D21

    # The number of NeoPixels
    num_pixels = 16

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=b, auto_write=False, pixel_order=ORDER
    )
    
    return pixels
    
def off(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(3)
    
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
        
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, b, g)

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

def cycle(wait, pixels, timeout = 5):
    duration = 0
    num_pixels = len(pixels)
    while duration < timeout:
        start = time.time()
        
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
                
            pixels.show()
            time.sleep(wait)
            stop = time.time()
            duration += ((stop-start)/100)
            
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

# slow_bright(pixels, color = (0,50,50))
# off(pixels)
# slow_bright(pixels, color = (75,75,100))
# pixels = setup_neopixel()

# # Open Box
pixels = setup_neopixel(b = 0.2)
# slow_bright(pixels, color = (0,90,120), t = 10,dt = .2)
# cycle_purple(0.001, pixels, t = 10)
# off(pixels)

# Luomous
slow_bright(pixels, color = (120,120,95), t = 10,dt = .2)
time.sleep(5)
off(pixels)

