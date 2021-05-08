from shapedetection import ShapeDetector
import argparse
import imutils
import cv2

# Setup some argument parsing so users can indicate file path of the image using "-i"
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="Argument requires providing the path to the image you wish to run the shape detection on.")

args = vars(ap.parse_args())

# Firstly, read in the image itself
image = cv2.imread(args["image"])

# Pre-processing stage
# Resize the image to make processing easier and faster
resized = imutils.resize(image, width = 300)
ratio = image.shape[0] / float(resized.shape[0])

# Grayscale the image to get rid of any color
grayimage = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Add some gaussian blur to smooth out the edges
blurredimage = cv2.GaussianBlur(grayimage, (5, 5), 0)

# Perform some thresholding, i.e set everything except the shape to black
# 1st arg is the input grayscale img, 2nd is the threshold (under which everything is set to black), 3rd is the max val
# Lastly, the 4th arg is the thresholding method, in this case, just a step function (i.e everything is either black or white, no shades)
threshimage = cv2.threshold(blurredimage, 60, 255, cv2.THRESH_BINARY)[1]

# Find the contours inside of the pre-processed image
contours = cv2.findContours(threshimage.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

contours = imutils.grab_countours(contours)

# Initialize the shape detector
sd = ShapeDetector()
print("The following shapes were detected : ")

# Shape Detection
for contour in contours:
    # First, we need the center of the counter
    M = cv2.moments(contour)

    # Essentially just finding the x and y coordinate of the center of the contour
    XCoord = int((M["m10"] / M["m00"]) * ratio)
    YCoord = int((M["m01"] / M["m00"]) * ratio)

    # Now to detect the shape
    shape = sd.detect(contour)
    print(shape)

    # FOR TESTING PURPOSES, DO NOT INCLUDE IN FINAL VERSION
    # Perform some resizing, draw a bounding box and place the name of the shape onto the image
    contour = contour.astype("float")
    contour *= ratio
    contour = contour.astype("int")
    cv2.drawContours(image, shape, (XCoord, YCoord), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Now show the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)



