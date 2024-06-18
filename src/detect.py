#!/usr/bin/env python3

print('Please run under desktop environment (eg: vnc) to display the image window')

import cv2
from picamera2 import Picamera2
import numpy as np
import time

color_dict = {'red': [0, 4], 'orange': [5, 18], 'yellow': [22, 37], 'green': [42, 85], 'blue': [92, 110],
              'purple': [115, 165],
              'red_2': [165, 180]}  # Here is the range of H in the HSV color space represented by the color

kernel_5 = np.ones((5, 5), np.uint8)  # Define a 5×5 convolution kernel with element values of all 1.


def color_detect(img, color_name):
    # The blue range will be different under different lighting conditions and can be adjusted flexibly.  H: chroma, S: saturation v: lightness
    resize_img = cv2.resize(img, (160, 120),
                            interpolation=cv2.INTER_LINEAR)  # In order to reduce the amount of calculation, the size of the picture is reduced to (160,120)
    hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)  # Convert from BGR to HSV
    color_type = color_name

    mask = cv2.inRange(hsv, np.array([min(color_dict[color_type]), 60, 60]), np.array([max(color_dict[color_type]), 255,
                                                                                       255]))  # inRange()：Make the ones between lower/upper white, and the rest black
    if color_type == 'red':
        mask_2 = cv2.inRange(hsv, (color_dict['red_2'][0], 0, 0), (color_dict['red_2'][1], 255, 255))
        mask = cv2.bitwise_or(mask, mask_2)

    morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5,
                                        iterations=1)  # Perform an open operation on the image

    # Find the contour in morphologyEx_img, and the contours are arranged according to the area from small to large.
    _tuple = cv2.findContours(morphologyEx_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # compatible with opencv3.x and openc4.x
    if len(_tuple) == 3:
        _, contours, hierarchy = _tuple
    else:
        contours, hierarchy = _tuple

    color_area_num = len(contours)  # Count the number of contours

    if color_area_num > 0:
        for i in contours:  # Traverse all contours
            x, y, w, h = cv2.boundingRect(
                i)  # Decompose the contour into the coordinates of the upper left corner and the width and height of the recognition object

            # Draw a rectangle on the image (picture, upper left corner coordinate, lower right corner coordinate, color, line width)
            if w >= 8 and h >= 8:  # Because the picture is reduced to a quarter of the original size, if you want to draw a rectangle on the original picture to circle the target, you have to multiply x, y, w, h by 4.
                x = x * 4
                y = y * 4
                w = w * 4
                h = h * 4
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a rectangular frame
                cv2.putText(img, color_type, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                            2)  # Add character description

    return img, mask, morphologyEx_img, contours

def classify_shape(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    
    # determine the shape based on the numbers of approx
    if len(approx) == 3:
        return "Triangle"
    elif len(approx) == 4:
        # 比率不同的情况是矩形
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        return "Square" if ar >= 0.95 and ar <= 1.05 else "Rectangle"
    elif len(approx) > 4:
        return "Circle"
    return "Unknown"

def shape_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    _, mask = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    
    kernel_5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5, iterations=1)
    
    # find contours
    contours, _ = cv2.findContours(morphologyEx_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_img = image.copy()
    
    for contour in contours:
        shape = classify_shape(contour)
        
        # draw contours
        cv2.drawContours(contours_img, [contour], -1, (0, 255, 0), 2)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(contours_img, shape, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return image, mask, morphologyEx_img, contours

