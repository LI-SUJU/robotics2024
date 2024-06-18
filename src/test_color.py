import cv2
from picamera2 import Picamera2
import numpy as np
from detect import color_detect

def rotate_move_rotate_touch():
    with Picamera2() as camera:
        camera.preview_configuration.main.size = (640, 480)
        camera.preview_configuration.main.format = "RGB888"
        camera.preview_configuration.align()
        camera.configure("preview")
        camera.start()
        is_touch = False
        
        while not is_touch:
            # capture the image
            img = camera.capture_array() 
            diff_tolerance = 50
            img, img_2, img_3, contours = color_detect(img, 'red')
            cv2.imshow("video", img)  
            cv2.imshow("mask", img_2) 
            cv2.imshow("morphologyEx_img", img_3) 

            k = cv2.waitKey(1) & 0xFF
            # 27 is the ESC key, which means that if you press the ESC key to exit
            if k == 27:
                break

        cv2.destroyAllWindows()
        camera.close()
  
rotate_move_rotate_touch()