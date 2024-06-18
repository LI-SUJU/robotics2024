import time
import picar_4wd as fc
import random
import obstacle_avoidance
from detect import detect1, contour_pos1

import cv2
from picamera2 import Picamera2
import numpy as np
# from detect import color_detect



power_val = 1


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
    print("停止")


def detect():
    with Picamera2() as camera:
        print("start color detect")

        camera.preview_configuration.main.size = (640, 480)
        camera.preview_configuration.main.format = "RGB888"
        camera.preview_configuration.align()
        camera.configure("preview")
        camera.start()
        is_touch = False

        print("!")

        # capture the image
        img = camera.capture_array()
        diff_tolerance = 50
        print("2")
        img, img_2, img_3, contours = detect1.color_detect(img, 'red')
        cv2.imshow("video", img)
        cv2.imshow("mask", img_2)
        cv2.imshow("morphologyEx_img", img_3)
        print("3", contours)


        percentage = contour_pos1.calculate_object_percentage_in_image(img, contours)

        # k = cv2.waitKey(1) & 0xFF
        # # 27 is the ESC key, which means that if you press the ESC key to exit
        # if k == 27:
        #     break

        print('quit ...')
        cv2.destroyAllWindows()
        camera.close()

        return percentage

# detect()

def move_close():
    # global movement_log
    start_time = time.time()
    move("forward", 5)
    duration = time.time() - start_time
    # movement_log.append(("forward", duration))
    stop()
    print("move_close_to_red")


def rotate_to_middle():
    # global movement_log
    start_time = time.time()
    move("turn_right", 5)
    duration = time.time() - start_time
    # movement_log.append(("turn_right", duration))
    stop()
    print("rotate_to_middle_red")


def move_to_touch():
    # global movement_log
    start_time = time.time()
    move("forward", 5)
    time.sleep(0.2)
    # duration = time.time() - start_time
    # movement_log.append(("forward", duration))
    stop()
    print("move_to_touch_red")


def spiral_search(duration):
    start_time = time.time()
    move_distance = 1  # 初始移动距离
    while time.time() - start_time < duration:
        for _ in range(2):  # 每次直行和转向两次，形成螺旋
            move('forward', power_val)
            forward_time = move_distance / power_val
            time.sleep(forward_time)
            stop()

            # 转向90度
            move('turn_right', power_val)
            time.sleep(1)
            stop()

        move_distance += 1  # 增加移动距离

        if detect() > 0:  # 如果检测到目标
            print("目标检测到，停止螺旋搜索")
            stop()
            return True
        if obstacle_avoidance.is_obstacle_detected():  # 如果检测到障碍物
            print("检测到障碍物，避开")
            obstacle_avoidance.obstacle_avoiding()  # 调用避障逻辑

    return False  # 未找到目标，搜索结束


def approach_target():
    while True:
        move('forward', power_val)
        percentage = detect()
        if percentage <= 0:  # 如果丢失目标
            print("目标丢失，重新开始螺旋搜索")
            stop()
            return False  # 目标丢失，重新搜索
        if percentage >= 0.5:  # 如果接触到目标
            print("目标已触碰，停止前进")
            stop()
            return True  # 目标已触碰，终止
        if obstacle_avoidance.is_obstacle_detected():  # 如果检测到障碍物
            print("检测到障碍物，避开")
            obstacle_avoidance.obstacle_avoiding()  # 调用避障逻辑
        time.sleep(0.1)

def main():
    search_duration = 60  # 搜索时间，例如60秒

    print("开始螺旋搜索...")
    while True:
        found = spiral_search(search_duration)
        if found:
            print("目标已找到，朝目标方向前进...")
            target_reached = approach_target()
            if target_reached:
                print("程序终止，已触碰到目标")
                break  # 程序终止
            else:
                print("目标丢失，重新开始螺旋搜索")
        else:
            print("未找到目标，继续螺旋搜索...")
            continue  # 未找到目标，继续螺旋搜索


if __name__ == "__main__":
    main()

