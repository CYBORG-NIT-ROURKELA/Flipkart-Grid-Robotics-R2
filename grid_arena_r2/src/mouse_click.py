#!/usr/bin/env python3

import cv2 as cv
import argparse


def click_event(event, x, y, flags, params):
    font = cv.FONT_HERSHEY_SIMPLEX

    if event == cv.EVENT_LBUTTONDOWN:
        print(x, y)
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(image, "{}, {}".format(x, y), (x,y), font, 1, (255, 0, 0), 2)

    if event==cv.EVENT_RBUTTONDOWN:
        print(x, y)
        b = self.image[y, x, 0]
        g = self.image[y, x, 1]
        r = self.image[y, x, 2]
        cv.putText(image, "{}, {}, {}".format(b, g, r), (x,y), font, 1, (255, 255, 0), 2)
    cv.imshow('image', image)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, help="image path")
    parser.add_argument('-v', '--video', type=str, help="video path or device port index")
    args = parser.parse_args()

    if args.image:
        image = cv.imread(args.image)
        cv.imshow('image', image)
        cv.setMouseCallback('image', click_event)
        cv.waitKey(0)

    elif args.video:
        source = int(args.video) if args.video.isnumeric() else args.video
        cap = cv.VideoCapture(source, cv.CAP_V4L)

        while cap.isOpened:
            ret, image = cap.read()
            if not ret:
                break
            cv.imshow('image', image)
            cv.setMouseCallback('image', click_event)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
    cv.destroyAllWindows()
