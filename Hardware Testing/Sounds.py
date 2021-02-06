import pygame
import time

def play_sound(filename):
    path = '/home/pi/Desktop/Raspberry_Potter/Rb_potter_files/Sounds'
    filepath = path + '//' + filename

    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    
def thread_function():
    for i in range(10):
        print(i)
        time.sleep(0.5)
        
play_sound('Lumos Maxima  HP (2).mp3')
thread_function()