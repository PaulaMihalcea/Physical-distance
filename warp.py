import sys
import cv2
import numpy as np
from get_dst_dim import get_dst_dim
from screeninfo import get_monitors


def warp(img_src, ratio, pts_src, show=False):

    # WARP
    dst_width, dst_height = get_dst_dim(pts_src, ratio)  # Calculate dimensions of destination image
    pts_dst = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]])  # Set destination points

    h, status = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    img_dst = np.zeros((img_src.shape[0], img_src.shape[1], 3), np.uint8)  # Create output image
    img_dst = cv2.warpPerspective(img_src, h, (dst_width, dst_height))  # Warp source image based on homography

    # DISPLAY RESOLUTION
    disp = []  # Monitor info list

    for m in get_monitors():  # Cycle on monitors found by the screeninfo library
        info = str(m)
        disp.append(info[info.find('DISPLAY1'):info.find('DISPLAY1')+8].strip())  # Get monitor name

    for i in range(0, len(disp)):  # Get width and height of main monitor; it is assumed to be the first that appears in the list
        if disp[i] == 'DISPLAY1':
            disp_width = int(info.split(',')[2].split('=')[1])
            disp_height = int(info.split(',')[3].split('=')[1])

    disp_tolerance = 50  # If the warped image is too large, an amount of pixels equal to this number will be left around the image window, so as to avoid occupying the whole screen
    img_dst_width = disp_width - disp_tolerance
    img_dst_height = disp_height - disp_tolerance

    if img_dst.shape[1] > img_dst_width:  # Resize warped image window if its width is larger than the screen width
        y = int(img_dst.shape[0] / (img_dst.shape[1] / img_dst_width))
        img_dst = cv2.resize(img_dst, (img_dst_width, y))
    elif img_dst.shape[0] > img_dst_height:  # Resize warped image window if its height is larger than the screen height
        x = int(img_dst.shape[1] / (img_dst.shape[0] / img_dst_height))
        img_dst = cv2.resize(img_dst, (x, img_dst_height))

    # DISPLAY RESULT (default: False)
    if show:
        cv2.imshow('', img_dst)  # Display warped image
        k = cv2.waitKey(0)
        if k == 27:  # ESC
            print('Exiting program...')
            sys.exit()  # Exit program

    return img_dst, h
