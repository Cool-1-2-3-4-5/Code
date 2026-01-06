import cv2 as cv
import numpy as np

# 1. Reading Images
# image = cv.imread('Images/Birds.jpg')
# cv.imshow("CHECK",image)
# cv.waitKey(0)

# # 2. Read webcam (or video)
cap = cv.VideoCapture(0) # intialize
while True:
    check, frame = cap.read() # function redes vudeo/webcam and return bool(frame was succefull or not) and frame
    cv.imshow("Vid",frame)
    if cv.waitKey(2) & 0xFF == ord('d'): # id d is pressed and 
        break
cap.release()  # destroys memroy asssociated with opening wideo
cv.destroyAllWindows

# # 3 Basic operation:
# # Resize:
# resized_img = cv.resize(image,(500,500))
# cv.imshow("New",resized_img)
# cv.waitKey(0)
# # Crop:
# cropped_img = image[100:200,50:200]
# cv.imshow("New",cropped_img)d
# cv.waitKey(0)


# # 4. Convert colour:
# gray_version = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
# cv.imshow("Gray",gray_version)
# cv.waitKey(0)

# # 5. Threshold (converty o remove discrepncies, perfect with gray scale)
# isTrue, new_frame = cv.threshold(gray_version,80,200,cv.THRESH_BINARY) # Parametres: image,lower range, upper range,type) in inverse anything less thna rdg value goes to 0 and reverse for other
# cv.imshow("Threshold", new_frame)
# cv.waitKey(0)

# # 5.1 Adaptive Threshold (Reular but better, threshold is different for each pixel)
# new_frame = cv.adaptiveThreshold(gray_version,300,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,21,30) # Parametres: image,lower range, upper range,type) in inverse anything less thna rdg value goes to 0 and reverse for other
# cv.imshow("adaptiveThreshold", new_frame)
# cv.waitKey(0)

# # 6. Edge Detection
# 3 types but use Canny
# edges = cv.Canny(image,280,30)
# cv.imshow("EDGES",edges)
# cv.waitKey(0)

# # 7. Contours and bounding boxes (For white space, makes lines around them)
# gray_version = cv.cvtColor(resized_img,cv.COLOR_BGR2GRAY)
# cv.imshow("Gray", gray_version)
# blurred = cv.GaussianBlur(gray_version, (5, 5), 0)
# cv.imshow("After Blur", blurred)
# thres = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
# # isTrue, thres = cv.threshold(blurred, 127, 255, cv.THRESH_BINARY_INV)
# cv.imshow("Threshold", thres)
# countours, hierachry = cv.findContours(thres, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# for i in countours:
#     area = cv.contourArea(i)
#     print(area)
#     if area > 100:
#         x, y, width, height = cv.boundingRect(i)
#         cv.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
# cv.imshow("BoundingBox", image)
# cv.waitKey(0)



### EXAMPLES

# # 1. Reading red on webcam:
# cap = cv.VideoCapture(0) # intialize
# while True:
#     check, frame = cap.read() # function redes video/webcam and return bool(frame was succefull or not) and frame
#     hue = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
#     colour_lower = np.array([0,130,80])
#     colour_higher = np.array([20,255,255])
#     object = cv.inRange(hue, colour_lower, colour_higher)
#     countours, hierachry = cv.findContours(object, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     for i in countours:
#         area = cv.contourArea(i)
#         print(area)
#         if area > 100:
#             x, y, width, height = cv.boundingRect(i)
#             cv.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
#     cv.imshow("Vid",frame)
#     if cv.waitKey(2) & 0xFF == ord('d'): # id d is pressed and 
#         break
# cap.release()  # destroys memroy asssociated with opening wideo
# cv.destroyAllWindows
