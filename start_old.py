import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import json
from send_data import Transport
rc_control = {"speed":0,"steering":0,"direction":0}
def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    #print(f"Intercept: {intercept}, Slope: {slope}")
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 -intercept)/slope)
    return np.array([x1,y1,x2,y2])
def average_middle_intercept(image,lines):
    image = np.zeros_like(image)
    lx1, ly1, lx2, ly2 = lines[0].reshape(4)
    rx1, ry1, rx2, ry2 = lines[1].reshape(4)
    middle_point = int((rx2+lx2)/2)
    image = cv2.line(image, (640, 720) , (middle_point, 432), (255,0,0), 10)
    angle = (np.arctan((middle_point-640)/432)*180/3.14)
    #print("METHOD1:", angle)
    return angle

#Alternative method for steering angle calculation [FINISHED]

def average_middle_intercept_2(image,lines):
    image = np.zeros_like(image)
    lx1, ly1, lx2, ly2 = lines[0].reshape(4)
    rx1, ry1, rx2, ry2 = lines[1].reshape(4)
    middle_point = int((rx2+lx2)/2)
    image = cv2.line(image, (640, 720) , (middle_point, 432), (255,0,0), 10)
    angle = 0
    # Car-parameters
    l = 0.28 #wheelbase in meters
    y = l + 0.31 #Distance from back axis to middle_point in meters
    x = float((middle_point - 640) * (0.32/457)) #Distance in x-direction from middle_point to cars direction in meters (32cm/457 pixels "scaling factor)
    if abs(x) > 0.01:
        angle = np.arctan((2*l)/float(x+y*y/x))*180/3.14
    #print(f"x: {x}")
    #print(f"Midpoint: {middle_point}")
    #print(f"METHOD2: {angle}")
    return angle
    
def average_slope_intercept(image,lines):
    left_fit = []
    right_fit = []
    left_line = [0,0,0,0]
    right_line = [0,0,1280,0]
    if lines is not None: 
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2), (y1,y2), 1)
            slope = parameters[0]
            if slope < 0.0001 and slope > 0: 
                slope = 0.0001
            elif slope > -0.0001 and slope < 0:
                slope = -0.0001
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope,intercept))
            else:
                right_fit.append((slope,intercept))
            if left_fit:
                left_fit_average = np.average(left_fit, axis = 0)
                left_line = make_coordinates(image, left_fit_average)
            if right_fit:
                right_fit_average = np.average(right_fit, axis = 0)
                right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    image = np.zeros_like(image)
    if lines is not None: 
        for x1, y1, x2, y2 in lines:
            print(f"X1: {x1}, Y1: {y1}, X2: {x2}, Y2: {y2}")
            cv2.line(image, (x1, y1), (x2, y2), (0,0,255), 10)
    return image


def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    polygons = np.array([
        [(0, height), (width, height), (550,250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

# image = cv2.imread('test_image.jpg')
# lane_image = np.copy(image)
# canny_img = canny(lane_image)
# cropped_image = region_of_interest(canny_img)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)
# average_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, average_lines)
# combo_image = cv2.addWeighted(lane_image,0.8, line_image, 1, 1)
# cv2.imshow("result", combo_image)
# cv2.waitKey(0)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
#cap.open()
send = Transport()
while(cap.isOpened()):
    _, frame = cap.read()  
    canny_img = canny(frame)
    cropped_image = region_of_interest(canny_img)
    cv2.imshow("cropped", cropped_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 10, maxLineGap = 5)
    average_lines = average_slope_intercept(frame, lines)  # Here we retrieve the lines
    #print(average_lines)
    #average_middle_intercept(frame, average_lines)
        #Calculate target point
            # [x1,y1,x2,y2] Use the average of x2,y2 from left and right lines
    #middle_line = average_middle_intercept(frame, average_lines)
    #combo_middle_image = cv2.addWeighted(frame,0.9, middle_line, 1, 1)
    line_image = display_lines(frame, average_lines)
    combo_image = cv2.addWeighted(frame,0.9, line_image, 1, 1)
    cv2.imshow("result", combo_image)
    turn_degree =  int(average_middle_intercept(frame, average_lines))
    if turn_degree < 15 and turn_degree > 0  or turn_degree > -15 and turn_degree < 0:
        speed=2
    else:
        speed = 2
    rc_control["steering"] = int(average_middle_intercept(frame, average_lines))
    rc_control["speed"] = speed
    #rc_control["steering"] = average_middle_intercept_2(frame, average_lines)
    #print(sys.getsizeof(json.dumps(rc_control)))
    #print(json.dumps(rc_control))
    send.send_data(json.dumps(rc_control))
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()  