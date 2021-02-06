# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:51:23 2020

@author: John
"""

import numpy as np
import cv2
import os
import time

#%% Create Blob Detector

# Define parameters for the required blob
params = cv2.SimpleBlobDetector_Params()

# setting the thresholds
params.minThreshold = 75
params.maxThreshold = 150

# filter by color
params.filterByColor = 1
params.blobColor = 255

# filter by circularity
params.filterByCircularity = 1
params.minCircularity = 0.5

# Filter by Convexity
params.filterByConvexity = 1;
params.minConvexity = 0.5;

# filter by area
params.filterByArea = 1
params.minArea = 30

# creating object for SimpleBlobDetector
detector = cv2.SimpleBlobDetector_create(params)

#%% Create Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

## List to hold coordinates of detected blobs
blob_points = []

# Frame Size
w_frame = 480;
h_frame = 640;

# Image Resize 
scale_percent = 15 # percent of original size
width = int(w_frame * scale_percent / 100)
height = int(h_frame * scale_percent / 100)
dim = (height,width)

im_save_fp = r'/home/pi/Documents/Raspberry_Potter/Rb_potter_files/Pictures'

im_name = "circle"

im_suffix = "%d.png"

im_name = im_name + im_suffix

count = 0 # count of frames
trace_len = 50 # number of frames 

# Create Blank Frame to Overlay key points
blank_image = np.zeros((w_frame,h_frame,3), np.uint8)

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret == False:
        break
    
    #Turn to gray scale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Remove background
    # frame = fgbg.apply(frame)
    
    # Detecting keypoints on video stream
    keypoints = detector.detect(frame)
    
    # Get coordinates of blob
    points_array = cv2.KeyPoint_convert(keypoints)
    
    # Initialize Points array
    if len(points_array) != 0:
        blob_points.append(points_array[0])
    
    # Draw the path by drawing lines between 2 consecutive points in points list
    for i in range(1, len(blob_points)):
        cv2.line(blank_image, tuple(blob_points[i-1]), tuple(blob_points[i]), (255, 255, 255), 3)
    
    # Truncate wand trace length and save image
    if len(blob_points) > trace_len:
        # Start new trace 
        blob_points = []
        
        # Rescale Image for Saving
        resized = cv2.resize(blank_image, dim, interpolation = cv2.INTER_AREA)
        
        # Save Old trace
        cv2.imwrite(os.path.join(im_save_fp, im_name) %count, resized)
    
        # Reset Blank Frame
        blank_image = np.zeros((w_frame,h_frame,3), np.uint8)    
    
        # Saved Image Count
        count+=1
        
        time.sleep(1.0)   
        
    cv2.imshow("frame",blank_image) 
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()
