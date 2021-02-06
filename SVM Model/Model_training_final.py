# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np
import sys
import os
import re
import math
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

#%% Functions
def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        # no deskewing needed.
        return img.copy()
    # Calculate skew based on central momemts.
    skew = m['mu11']/m['mu02']
    # Calculate affine transform to correct skewness.
    M = np.float32([[1, skew, -0.5*img.shape[0]*skew], [0, 1, 0]])
    # Apply affine transform
    img = cv2.warpAffine(img, M, (img.shape[0], img.shape[0]), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return img

def bbox_and_resize(img):

    # convert image to grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(gray,15,255,0)

    # apply bounding box around symbol
    x,y,w,h = cv2.boundingRect(thresh)

    bp = 4 # boarder pixels

    rs = (y-bp) # starting row
    re = (y+h+bp) # ending row
    cs = (x-bp) # starting col
    ce = (x+w+bp) # ending col

    rect = thresh[rs:re,cs:ce]

    try:
        resized = cv2.resize(rect,(25,25),interpolation = cv2.INTER_NEAREST)
    except:
        return cv2.resize(thresh,(25,25),interpolation = cv2.INTER_NEAREST)

    return resized

def plot_images(img_data,labels_predicted,label_actual):

    get_ipython().run_line_magic('matplotlib', 'qt')

    ncolrow = math.ceil(math.sqrt(len(img_data)))

    f = plt.figure()
    for i,img in enumerate(img_data):
        ax = f.add_subplot(ncolrow,ncolrow,i+1)
        ax.imshow(img, cmap = 'gray')
        ax.axis('off')

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.1)

    plt.show()

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

def data_gen_flip_x(img, label):

    # Just flip other images
    img_flip = np.flip(img.copy(),axis = 1)

    # Flip and rotate for Lshape
    if "Lshape" in label:
        img_flip = np.rot90(img_flip)

    return img_flip

#%% Prepare Images
# Change this to where images are stored
#  img_paths = r"D:\Engineering Projects\Harry Potter Wand Lamp\Raspberry_Potter\Rb_potter_files\Pictures"
img_paths = r"/home/pi/Desktop/Raspberry_Potter/Rb_potter_files/Pictures"

img_data = []
hog_desc = []
labels = []
hog = make_hog()

for path, subdirs, files in os.walk(img_paths):
    for name in files:

        img = cv2.imread(os.path.join(path, name))
        img_resize = bbox_and_resize(img)
        img_hog_desc = hog.compute(img_resize)

        # img_deskew = deskew(img_resize)
        # img_hog_desc = hog.compute(img_deskew)
        # img_data.append(img_deskew)

        img_data.append(img_resize)
        hog_desc.append(img_hog_desc)

        if "bad" in path:
            label = "bad"
        else:
            label = re.findall("([A-z]*)",name)[0]

        labels.append(label)

        # Gen data by flipping images
        img_flip = data_gen_flip_x(img_resize,label)
        img_hog_desc_flip = hog.compute(img_flip)

        img_data.append(img_flip)
        hog_desc.append(img_hog_desc_flip)
        labels.append(label)


# Remap Labels to numeric
le = preprocessing.LabelEncoder()
le.fit(labels)
labels_numeric = le.fit_transform(labels)

# combine data into one array
data = np.concatenate(hog_desc, axis = 1).T

# Create test and training sets
train_data, test_data, train_labels, test_labels = train_test_split(data,\
                                                                    labels_numeric,test_size=0.1)

#%% Train Model Open CV
# Set up SVM for OpenCV 3
svm = cv2.ml.SVM_create()
# Set SVM type
svm.setType(cv2.ml.SVM_C_SVC)
# Set SVM Kernel to Radial Basis Function (RBF)
svm.setKernel(cv2.ml.SVM_RBF)
# svm.setKernel(cv2.ml.SVM_LINEAR)

svm.trainAuto(train_data,cv2.ml.ROW_SAMPLE, train_labels)

# Save trained model
filepath = os.path.dirname(os.path.abspath(__file__))
filename = filepath + '//' + "svm_model_data_gen_rbpi.yml"

svm.save(filename)

#%% Test Model
testResponse = svm.predict(test_data, True)[1].ravel()

test_labels_predicted = le.inverse_transform(testResponse.astype(int))
test_labels_actual = le.inverse_transform(test_labels.astype(int))

acc_array =  np.equal(testResponse.astype(int),test_labels.astype(int))

accuracy = acc_array.astype(int)

print("Accuracy: % 5.2f" %(100*(np.sum(accuracy)/accuracy.shape[0])),"%")

print("MisClassfied")
print("Predicted: ", test_labels_predicted[np.where(acc_array == False)])
print("Actual: ", test_labels_actual[np.where(acc_array == False)])

svm_load = cv2.ml.SVM_load(filename)

testResponse = svm_load.predict(test_data, True)[1].ravel()

test_labels_predicted = le.inverse_transform(testResponse.astype(int))
test_labels_actual = le.inverse_transform(test_labels.astype(int))

acc_array =  np.equal(testResponse.astype(int),test_labels.astype(int))

accuracy = acc_array.astype(int)

print("Accuracy Loaded: % 5.2f" %(100*(np.sum(accuracy)/accuracy.shape[0])),"%")

print("MisClassfied")
print("Predicted: ", test_labels_predicted[np.where(acc_array == False)])
print("Actual: ", test_labels_actual[np.where(acc_array == False)])


#%% Test Flipping
index = 110

img = img_data[index]

label = labels[index]

img_flip = data_gen_flip_x(img, label)

get_ipython().run_line_magic('matplotlib', 'qt')

plt.figure(2)
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
ax1.imshow(img)
ax2.imshow(img_flip)

plt.show()