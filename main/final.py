from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import numpy as np
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Prompt for the width of the reference object
width = float(input("Enter the width of the left-most object in the video (in inches): "))

# Initialize the webcam video stream
vs = cv2.VideoCapture(0)

# Initialize the pixels per metric calibration variable
pixelsPerMetric = None

while True:
    # Read the current frame from the webcam
    ret, frame = vs.read()
    if not ret:
        break
    
    # Convert the frame to grayscale and blur it slightly
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Perform edge detection, then dilate and erode to close gaps
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # Find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Sort contours from left to right
    (cnts, _) = contours.sort_contours(cnts)

    # Loop over the contours individually
    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        # Compute the rotated bounding box of the contour
        orig = frame.copy()
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)  # Use cv2.boxPoints for OpenCV 3.0 and above
        box = np.array(box, dtype="int")

        # Order the points in the bounding box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # Draw points and midpoints
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        # Draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

        # Compute the Euclidean distances
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # Initialize pixels per metric if not already done
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / width

        # Compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        # Draw the object sizes on the image
        cv2.putText(orig, "{:.1f}in".format(dimA), (int(tltrX - 15), int(tltrY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.1f}in".format(dimB), (int(trbrX + 10), int(trbrY)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        # Show the output image
        cv2.imshow("Frame", orig)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
vs.release()
cv2.destroyAllWindows()