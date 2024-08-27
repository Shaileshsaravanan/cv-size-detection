import cv2
import cv2.aruco as aruco
import numpy as np
from object_detector import detectorObj

# Load Aruco detector
parameters = aruco.DetectorParameters()
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

# Load Object Detector
detector = detectorObj()

# Load Cap
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, img = cap.read()

    # Get Aruco marker
    corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if corners:
        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

        # Calculate Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0][0], True)
        print(f"Aruco Perimeter (in pixels): {aruco_perimeter}")

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20  # 20 is the perimeter for a 5x5 cm marker
        print(f"Pixel to cm ratio: {pixel_cm_ratio}")

        contours = detector.detect_objects(img)

        # Draw objects boundaries
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect

            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio
            print(f"Detected object width: {object_width}, height: {object_height}")

            # Display rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img, [box], True, (255, 0, 0), 2)
            cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()