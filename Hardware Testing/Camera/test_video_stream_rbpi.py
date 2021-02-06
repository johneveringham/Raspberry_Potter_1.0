# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:51:23 2020

@author: John
"""

import numpy as np
import cv2
import os
import time

#%% 
# Capture Frame
# Remove Background
# Detect Blob
# Store Blob location
# every x num of frames store blob shape
# if blob shape = spell shape, do something
# store blob shape into array
# save 

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

## List to hold coordinates of detected blobs and hold list of blob points
blob_points = []

# Frame Size
w_frame = 480;
h_frame = 640;

#%% Normal Video Stream
cap = cv2.VideoCapture(r'D:\Engineering Projects\Harry Potter Wand Lamp\Test_video\video.h264')

count = 0
trace_len = 50

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
    if len(blob_points) > trace_len:
        # Start new trace 
        blob_points = []
    
        count+=1
        
        time.sleep(1.0)   
        
    cv2.imshow("frame",frame_with_keypoints) 
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()

#%% Process and Save 

points_array[0]
