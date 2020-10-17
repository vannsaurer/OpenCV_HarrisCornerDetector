# OpenCV_HarrisCornerDetector
This program demonstrates a Harris Corner Detector algorithm using the OpenCV library.

Author: Virginia Saurer 

Date: March 18 2020

As a result, 4 windows of the the box_in_scene.png image open depicting each stage of the Harris Corner Detector algorithm run on the image. 

The first window depicts the original image.

The next window depicts the black and white pixel image of the detected corners at threshold 0.01.

The third window depicts the same black and white pixel image but with applied non-maximum suppression. 

The final window shows the original image with the threshold trackbar slider. It starts out showing the corners in the image with the applied 0.01 threshold. The user can then move the threshold slider, between 1 and 10, to see the different corner detection results of the various applied thresholds.

Files included in folder HarrisCornerDetector_Part1: 
harrisCornerDet.py
box_in_scene.png


To run program: python harrisCornerDet.py


To end the program close all the windows

A Snapshot of the end result of the code is in the pdf document Snapshot_of_HarrisCornerDetector.pdf

