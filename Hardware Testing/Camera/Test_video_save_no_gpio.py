import picamera     # Importing the library for camera module
from time import sleep  # Importing sleep from time library to add delay in program

time_record = 30; # seconds
save_location = r'/home/pi/Desktop/video.h264';

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    # Camera warm-up time
    sleep(5)
    
    print(" Capture Start")
    
    camera.start_preview()      # You will see a preview window while recording
    camera.start_recording(save_location) # Video will be saved at desktop
    sleep(time_record)
    camera.stop_recording()
    camera.stop_preview()

    print(" Capture Complete")
 