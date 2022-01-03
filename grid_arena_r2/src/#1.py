#!/usr/bin/env python3

bot_ips = {
    2: '192.168.247.103',
    1: '192.168.134.82'
}

import socket
import cv2, argparse
import numpy as np
import time



def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = [bot_ips[args.tag_id]]
    i = 0
    ip_add = ip_address[i]
    print(ip_add)
    port = 4210

    # drop_flag = False
    # print(drop_flag)
    def forward(speed):
        print("forward")
        left_speed = speed
        right_speed = speed
        servo_angle = 0
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    def left(speed):
        print("left")
        left_speed = -speed
        right_speed = 0
        servo_angle = 0
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    def right(speed):
        print("right")
        left_speed = 0
        right_speed = -speed
        servo_angle = 0
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    def back(speed):
        print("back")
        left_speed = -speed
        right_speed = -speed
        servo_angle = 0
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    def drop():
        print("drop")
        left_speed = 0
        right_speed = 0
        global drop_flag
        if not drop_flag:
            servo_angle = 180
        else:
            servo_angle = -180
        drop_flag = not drop_flag
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    def rotate(speed):
        print("rotate")
        left_speed = -speed
        right_speed = speed
        servo_angle = 0
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    def stop(speed = 0):
        print("stop")
        left_speed = speed
        right_speed = speed
        servo_angle = 0
        msg = "{},{},{}\r".format(left_speed, right_speed, servo_angle)
        sock.sendto(str.encode(msg), (ip_add, port))

    while True:
        blank = np.zeros((200,200,3), np.uint8)
        cv2.imshow("window", blank)
        key_pressed = cv2.waitKey(0)

        if key_pressed == ord('c'):
            i+=1
            if i>3:
                i = 0
            ip_add = ip_address[i]
            print("current_bot ",i+1, ip_add)

        if key_pressed == 255:
            stop(0)

        elif key_pressed == 82:
            back(1024)
            # stop()

        elif key_pressed == 83:
            right(1024)
            # stop()

        elif key_pressed == 84:
            forward(1024)
            # stop()

        elif key_pressed == 81:
            left(1024)
            # stop()

        elif key_pressed == ord('r'):
            rotate(1024)
            # stop()

        elif key_pressed == ord('d'):
            drop()

        elif key_pressed == 32:
            stop(0)

        elif key_pressed == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tag_id", nargs="?", type=int, default=1)

    args = parser.parse_args()
    main()
