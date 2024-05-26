import cv2
from picamera2 import Picamera2
import numpy as np

def analysis_image(img, contours, center_tolerance=50):
    """
    Args:
        center_error_percentage (float): [0,1] The allowable margin of error when comparing whether an object is centered.
    Returns:
        is_item_present(boolean): True if the object is detected, False otherwise.
        is_center(boolean):
        width_percentage (float): [0,1]
    """

    is_item_present = False
    center_state = 0
    width_percentage = 0

    image_width, image_width, c = img.shape

    color_area_num = len(contours)  # Count the number of contours

    if color_area_num > 0:
        # for i in contours:    # Traverse all contours
        x, y, w, h = cv2.boundingRect(contours[
                                          0])  # Decompose the contour into the coordinates of the upper left corner and the width and height of the recognition object
        x = x * 4
        y = y * 4
        w = w * 4
        h = h * 4

        centerX = round(image_width / 2)
        if x > centerX:
            center_state = 3
        elif x + w < centerX:
            center_state = 1
        else:
            diff = abs(abs(centerX - x) - abs(x + w - centerX))
            if centerX - x > x + w - centerX & diff > center_tolerance:
                center_state = 1
            elif centerX - x < x + w - centerX & diff > center_tolerance:
                center_state = 3
            else:
                center_state = 2

        width_percentage = w / image_width

    is_item_present = True if color_area_num > 0 else False

    return is_item_present, center_state, width_percentage


def detect_object_in_image(contours):
    # 
    color_area_num = len(contours)
    return True if color_area_num > 0 else False


def check_center_state(img, contours, center_tolerance=50):
    # 0 = None, 1 = Left, 2 = Center, 3 = Right
    if len(contours) == 0:
        return 0
    color_area_num = len(contours)
    image_width, image_width, c = img.shape

    if color_area_num > 0:
        x, y, w, h = cv2.boundingRect(contours[
                                          0])  # Decompose the contour into the coordinates of the upper left corner and the width and height of the recognition object
        x = x * 4
        y = y * 4
        w = w * 4
        h = h * 4

        centerX = round(image_width / 2)
        if x > centerX:
            return 3
        elif x + w < centerX:
            return 1
        else:
            diff = abs(abs(centerX - x) - abs(x + w - centerX))
            if centerX - x > x + w - centerX & diff > center_tolerance:
                return 1
            elif centerX - x < x + w - centerX & diff > center_tolerance:
                return 3
            else:
                return 2


def calculate_object_percentage_in_image(img, contours):
    color_area_num = len(contours)
    image_width, image_width, c = img.shape

    if color_area_num > 0:
        x, y, w, h = cv2.boundingRect(contours[
                                          0])  # Decompose the contour into the coordinates of the upper left corner and the width and height of the recognition object
        x = x * 4
        y = y * 4
        w = w * 4
        h = h * 4
        return w / image_width

