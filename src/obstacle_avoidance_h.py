import picar_4wd as fc

# speed = 30
speed = 5


def is_obstacle_detected():
    while True:

        scan_list = fc.scan_step(35)

        if not scan_list:
            continue
        tmp = scan_list[3:7]
        print("scan data:", tmp)
        if tmp != [2, 2, 2, 2]:
            print("obstacle detected!")
            return True
        else:
            return False


def obstacle_avoiding():
    print('obstacle_avoiding')
    is_obstacled = True
    fc.stop()
    while is_obstacled:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2, 2, 2, 2]:
            fc.turn_left(speed)
        else:
            is_obstacled = False

# def main():
#     while True:
#         scan_list = fc.scan_step(35)
#         if not scan_list:
#             continue

#         tmp = scan_list[3:7]
#         print(tmp)
#         if tmp != [2,2,2,2]:
#             fc.turn_right(speed)
#         else:
#             fc.forward(speed)

# if __name__ == "__main__":
#     try:
#         main()
#     finally:
#         fc.stop()
