import time
import picar_4wd as fc
import random
import sys
import tty
import termios
import signal
from obstacle_avoidance import is_obstacle_detected, obstacle_avoiding
from detect import color_detect
from contour_pos import calculate_object_percentage_in_image, analysis_image, check_center_state

import cv2
from picamera2 import Picamera2
import numpy as np

global power_val
global is_found
global is_searching 
global is_touch
power_val = 1
is_found = False
is_searching = False
is_touch = False

def move(action, power_val):
    if action == "forward":
        fc.forward(power_val)
    elif action == "backward":
        fc.backward(power_val)
    elif action == "turn_left":
        fc.turn_left(power_val)
    elif action == "turn_right":
        fc.turn_right(power_val)
    else:
        fc.stop()

def stop():
    fc.stop()
    
def turn_left():
    move("turn_left", 5)
    time.sleep(0.2)
    stop()

def go_forward():
    move("forward", 5)
    time.sleep(0.5)
    stop()

def turn_right():
    move("turn_right", 5)
    time.sleep(0.2)
    stop()

global move_distance
global distance_times
move_distance = 1 
distance_times = 0

def spiral_search():
    global move_distance
    global distance_times
    
    # go forward 10 times then turn right
    if(distance_times < 10):
        move('forward', power_val)
        # compute the move time based on the move distance to ensure go spiral
        forward_time = move_distance / power_val
        time.sleep(forward_time / 10)
        distance_times += 1
        stop()
    else:
        move('turn_right', power_val)
        time.sleep(0.1)
        stop()
        move_distance += 1  
        is_searching = False
        distance_times = 0
        stop()
    
def adjust_rotate(center_state):
    if center_state == 1:
        turn_left()
    elif center_state == 3:
        turn_right()
    else:
        go_forward()
        
def main():
    with Picamera2() as camera:
        camera.preview_configuration.main.size = (640, 480)
        camera.preview_configuration.main.format = "RGB888"
        camera.preview_configuration.align()
        camera.configure("preview")
        camera.start()
        is_touch = False

        while not is_touch:
            
            img = camera.capture_array()  # frame.array
            diff_tolerance = 50
            img, img_2, img_3, contours = color_detect(img, 'red')
            cv2.imshow("video", img) 
            cv2.imshow("mask", img_2) 
            cv2.imshow("morphologyEx_img", img_3) 

            is_item_present, center_state, width_percentage = analysis_image(img, contours, diff_tolerance)
            print("image state", is_item_present, center_state, width_percentage)
            
            # keep detecting obstacles when running
            if is_obstacle_detected() and not is_item_present:
                # avoid obstacles once detected
                obstacle_avoiding()

            if is_item_present:
                is_found = True
                if width_percentage < 0.2:
                    current_state = check_center_state(img, contours, 60)
                    adjust_rotate(current_state)
                elif width_percentage > 0.5:
                    # determine touched the target when the target is over 50% and stop the robot
                    stop()
                    is_touch = True
                else:
                    # adjust rotate to keep target is placing at the center
                    current_state = check_center_state(img, contours, 20)
                    adjust_rotate(current_state)

                k = cv2.waitKey(1) & 0xFF
                # 27 is the ESC key, which means that if you press the ESC key to exit
                if k == 27:
                    break
            else:
                is_found = False
                if not is_searching:
                    # keep spiral searching if not touch the target
                    spiral_search()

def signal_handler(sig, frame):
    # exit
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()

