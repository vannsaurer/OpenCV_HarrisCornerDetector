import numpy as np
import cv2

#Harris Corner Detection
#Virginia Saurer 101037563
#March 15 2020

midThreshold = 5
maxThreshold = 10

#The Harris Corner Detector function that takes in a threshold, in our case 0.01
def myHarrisCornerDetection(threshold):
    image_copy = np.copy(image)
    image_copy2 = np.copy(image)
    midThreshold = max(threshold, 1)

    #Thresholding the minimum eigenvalues
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #Checking the Eigenvalues
            #if the Eigenvalues pass the threshold test, the pixels that pass are coloured white otherwise black
            if minEigenValues[i,j] > threshold:#threshold = 0.01
                image_copy2[i, j] = 255
            else:
                image_copy2[i, j] = 0

            #Another way of checking the Eigen Values and drawing in circles where corners are detected
            if minEigenValues[i,j] > minEigen + ( maxEigen - minEigen )*(midThreshold)/maxThreshold:
                cv2.circle(image_copy, (j,i), 4,  (256,256), cv2.FILLED)

    cv2.imshow(HarrisCorner_window2, image_copy2)

    # convolve the corner detected image with Sobelx and Sobely kernels
    # this is to get the magnitude and gradient angle to pass intot the
    # non-maximum suppression function to thin the corner pixels
    convoleSobelx = cv2.Sobel(image_copy2, cv2.CV_32F, 1, 0)
    convoleSobely = cv2.Sobel(image_copy2, cv2.CV_32F, 0, 1)
    m, ang = cv2.cartToPolar(convoleSobelx, convoleSobely)

    # pass in the magnitude image and gradient angle into the non-maximum suppression function
    finalResult = myNonMaxSuppression(m, ang)
    cv2.imshow("The Corners with Non-Max Supression", finalResult)
    cv2.imshow(HarrisCorner_window, image_copy)
    cv2.waitKey()

#my non-max suppression function from Assignment 1
def myNonMaxSuppression(image, gradientA):
    row, col = image.shape
    nonMaxSupImage = np.zeros((row, col), dtype=np.float32)
    angle = gradientA * 180. / np.pi
    angle[angle < 0] += 180
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            try:
                q = 255
                r = 255
                # map the gradient angle to the closest of 4 cases,
				# where the line is sloped at almost 0, 45, 90 and 135 degrees
				# check at angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = image[i, j + 1]
                    r = image[i, j - 1]
                # check at angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = image[i + 1, j - 1]
                    r = image[i - 1, j + 1]
                # check at angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = image[i + 1, j]
                    r = image[i - 1, j]
                # check at angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = image[i - 1, j - 1]
                    r = image[i + 1, j + 1]

                # for each pixel look at the 2 neighboring pixels along the gradient direction and
				# if either of those pixels has a larger gradient magnitude then set the edge magnitude
				# at the center pixel to zero
                if (image[i, j] >= q) and (image[i, j] >= r):
                    nonMaxSupImage[i, j] = image[i, j]
                else:
                    nonMaxSupImage[i, j] = 0

            except IndexError as e:
                pass
    return nonMaxSupImage

# The Sobel x-axis kernel
sobelX = np.array((
	[-1, 0, 1],
	[-2, 0, 2],
	[-1, 0, 1]), dtype="float32")

# The Sobel y-axis kernel
sobelY = np.array((
	[-1, -2, -1],
	[0, 0, 0],
	[1, 2, 1]), dtype="float32")

#Read in the image
image = cv2.imread('C:/Users/Virginia Saurer/PycharmProjects/A1/box_in_scene.png', 0)
origImage_window = 'Original Image'
#show the original image in a window
cv2.imshow(origImage_window, image)

# Setting the parameters for the cornerMinEigenVal function
blockSize = 3
apertureSize = 3
#Calculating the minimum Eigenvalue of the image
minEigenValues = cv2.cornerMinEigenVal(image, blockSize, apertureSize)
#Calculating the min and max Eigen values of the image
minEigen, maxEigen, _, _ = cv2.minMaxLoc(minEigenValues)

#Naming the 3 corner detection windows that will be shown

#This window displays the original image with the corners being detected and indicated with white dots
HarrisCorner_window = 'Harris Corner Detector '

#This window displays only the corners of the orginal image, indicated with white pixels that passed
# the threshold test
HarrisCorner_window2 = 'The Corners at T = 0.01'

#This window displays the thined corners of the orginal image with non-maximum supression applied to the
# pixels that passed the threshold test
JustCorners_window = 'The Corners w nonMaxSupression'

cv2.namedWindow(HarrisCorner_window)

# Create Window and Trackbar to show the Threshold Test
#current midThreshold and maxThreshold are 5 and 10 respectively but....need to change those values
cv2.createTrackbar('T(0-10)', HarrisCorner_window, 0, maxThreshold, myHarrisCornerDetection)

#trackbar_name = 'Alpha x %d' % alpha_slider_max
#cv.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)
#Calling Harris Corner Function with threshold passed into it
myHarrisCornerDetection( 0.01)

cv2.waitKey()