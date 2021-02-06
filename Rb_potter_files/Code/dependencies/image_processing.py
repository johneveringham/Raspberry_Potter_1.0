import cv2
import numpy as np
import sys
import os
import re
import matplotlib.pyplot as plt

# For Blob Detector
def check_speed(point1,point2,time):
    # input: two blob points output true
    # if they are close enough and not traveling to fast
    p = np.sum((point1-point2)**2)
    dist = np.sqrt(p)
    velocity = dist/time
    #print("%5.2f" % velocity)
    
    if 500 < velocity > 50:
        check = True
    else:
        check = False
    
    return check

def create_blob_detector():
    
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
    params.minArea = 25
    params.maxArea = 150 

    # creating object for SimpleBlobDetector
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector

# For SVM Model
def bbox_and_resize(img):

    # apply bounding box around symbol
    x,y,w,h = cv2.boundingRect(img)

    bp = 4 # boarder pixels

    rs = (y-bp) # starting row
    re = (y+h+bp) # ending row
    cs = (x-bp) # starting col
    ce = (x+w+bp) # ending col

    rect = img[rs:re,cs:ce]

    try:
        resized = cv2.resize(rect,(25,25),interpolation = cv2.INTER_NEAREST)
    except:
        return cv2.resize(img,(25,25),interpolation = cv2.INTER_NEAREST)

    return resized

def make_hog():
    winSize = (25,25)
    blockSize = (10,10)
    blockStride = (5,5)
    cellSize = (10,10)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradients = True

    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize \
                            ,nbins,derivAperture,winSigma,histogramNormType \
                            ,L2HysThreshold,gammaCorrection,nlevels, signedGradients)
    return hog