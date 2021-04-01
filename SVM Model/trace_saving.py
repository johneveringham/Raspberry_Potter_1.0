# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:51:23 2020

@author: John
"""

import numpy as np
import cv2
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(1.0)

#%% Create Blob Detector

# Define parameters for the required blob
params = cv2.SimpleBlobDetector_Params()

# setting the thresholds
params.minThreshold = 170
params.maxThreshold = 250

# filter by color
params.filterByColor = 1
params.blobColor = 255

# filter by circularity
params.filterByCircularity = 1
params.minCircularity = 0.3

# Filter by Convexity
params.filterByConvexity = 1;
params.minConvexity = 0.3;

# filter by area
params.filterByArea = 1
params.minArea = 8
params.maxArea = 120 

# creating object for SimpleBlobDetector
detector = cv2.SimpleBlobDetector_create(params)

## List to hold coordinates of detected blobs and hold list of blob points
blob_points = []

# Frame Size
w_frame = 480;
h_frame = 640;

# Image Resize 
scale_percent = 15 # percent of original size
width = int(w_frame * scale_percent / 100)
height = int(h_frame * scale_percent / 100)
dim = (height,width)

im_save_fp = r'/home/pi/Desktop/Raspberry_Potter/Rb_potter_files/Pictures'

im_name = "random"

im_suffix = "%d.png"

print(os.path.join(im_save_fp, im_name))

im_name = im_name + im_suffix

count = 0
trace_len = 25
im_count = 0
im_count_limit = 50

# Create Blank Frame to Overlay key points
blank_image = np.zeros((w_frame,h_frame,3), np.uint8)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    frame = frame.array
      
    # Turn to gray scale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detecting keypoints on video stream
    keypoints = detector.detect(frame)
    
    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Get coordinates of blob
    points_array = cv2.KeyPoint_convert(keypoints)
    
    # Initialize Points array
    if len(points_array) != 0:
        blob_points.append(points_array[0])
    
    # Draw the path by drawing lines between 2 consecutive points in points list
    for i in range(1, len(blob_points)):
        cv2.line(blank_image, tuple(blob_points[i-1]), tuple(blob_points[i]), (255, 255, 255), 3)
        cv2.line(frame_with_keypoints, tuple(blob_points[i-1]), tuple(blob_points[i]), (255, 0, 0), 3)
        
    # show image for drawing trace  
    cv2.imshow("frame",frame_with_keypoints)
        
    # Truncate wand trace length and save image
    if count > trace_len:
        # Start new trace 
        blob_points = []
        
        # Rescale Image for Saving
        resized = cv2.resize(blank_image, dim, interpolation = cv2.INTER_AREA)
        
        # Save Old trace
        cv2.imwrite(os.path.join(im_save_fp, im_name) %im_count, resized)
        
        # Indicator that image was saved
        cv2.circle(blank_image, (int(w_frame/2), int(h_frame/2)),20,(0, 255, 0), 3)
        
        # frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Reset Blank Frame
        blank_image = np.zeros((w_frame,h_frame,3), np.uint8)    
    
        time.sleep(3.0)
        
        im_count += 1
        
        count = 0
        
        if im_count > im_count_limit:
            break 
    
    count+=1
    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
