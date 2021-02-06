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
params.minThreshold = 150
params.maxThreshold = 250

# filter by color higher number = lighter
params.filterByColor = True
params.blobColor = 255

# filter by circularitycloser to 1 equal circle
params.filterByCircularity = True
params.minCircularity = 0.3

# Filter by Convexity
params.filterByConvexity = True;
params.minConvexity = 0.3;

# filter by area
params.filterByArea = True
params.minArea = 5

# creating object for SimpleBlobDetector
detector = cv2.SimpleBlobDetector_create(params)

#%% Create Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

## List to hold coordinates of detected blobs and hold list of blob points
blob_points = []

# Frame Size
w_frame = 480;
h_frame = 640;

count = 0
trace_len = 25

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    frame = frame.array
      
    #Turn to gray scale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Remove background
    # frame = fgbg.apply(frame)
    
    # Detecting keypoints on video stream
    keypoints = detector.detect(frame)
    
    # Plot keypoints on Blank frame
    # frame_with_keypoints = cv2.drawKeypoints(blank_image, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    points_array = cv2.KeyPoint_convert(keypoints)
    
    # Initialize Points array
    if len(points_array) != 0:
        blob_points.append(points_array[0])
    
    # Draw the path by drawing lines between 2 consecutive points in points list
    for i in range(1, len(blob_points)):
        # cv2.line(blank_image, tuple(blob_points[i-1]), tuple(blob_points[i]), (255, 255, 0), 3)
        cv2.line(frame_with_keypoints, tuple(blob_points[i-1]), tuple(blob_points[i]), (255, 0, 0), 3)
    
    # Truncate wand trace length and save image
    if count > trace_len:
        # Start new trace 
        blob_points = []
    
        time.sleep(1.0)
        
        count = 0
        
    cv2.imshow("frame",frame_with_keypoints) 
    
    count+=1
    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
