import cv2
from picamera2 import Picamera2
import numpy as np
from detect import color_detect

def rotate_move_rotate_touch():
    with Picamera2() as camera:
        print("start color detect")

        camera.preview_configuration.main.size = (640, 480)
        camera.preview_configuration.main.format = "RGB888"
        camera.preview_configuration.align()
        camera.configure("preview")
        camera.start()
        is_touch = False
        
        print("!")

        while not is_touch:
            # capture the image
            img = camera.capture_array() 
            diff_tolerance = 50
            print("2")
            img, img_2, img_3, contours = color_detect(img, 'red')
            cv2.imshow("video", img)  
            cv2.imshow("mask", img_2) 
            cv2.imshow("morphologyEx_img", img_3) 
            print("3", contours)
            

            # if is_item_present:
            #     if width_percentage < 0.2:
            #         # If the target is far away, allow a larger tolerance when detecting the center state
            #         current_state = check_center_state(img, contours, 60)
            #         print("far", current_state)
            #         adjust_rotate(current_state)
            #     elif width_percentage > 0.7:
            #         # Assume that the target object has been touched when it occupies 70% of the field of view.
            #         stop()
            #         is_touch = True
            #     else:
                        #         current_state = check_center_state(img, contours, 20)
            #         print("close", current_state)
            #         adjust_rotate(current_state)

            k = cv2.waitKey(1) & 0xFF
            # 27 is the ESC key, which means that if you press the ESC key to exit
            if k == 27:
                break
            # else:
            #     turn_right()

        print('quit ...')
        cv2.destroyAllWindows()
        camera.close()
  
rotate_move_rotate_touch()