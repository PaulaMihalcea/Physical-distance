import sys
import cv2
import numpy as np
from get_dst_dim import get_dst_dim
from screeninfo import get_monitors
from utils import get_pts


def is_int(n):
    try:
        n = int(n)
        return n
    except ValueError:
        return None


def get_click_src(img_src):

    # VARIABLES
    pts_src = None  # Source points
    img_src_b = img_src.copy()  # Image with border

    # GET POINTS BY CLICK
    while True:  # Wait for four valid source points

        print('Click on the four points of the floor plane (top left, top right, bottom right, bottom left) then press ENTER,\n'
              'or press SPACEBAR to add or change borders.\n'
              'Otherwise, press ESC to exit.')
        print('')

        pts_src = get_pts(img_src_b)

        if pts_src is not None:  # Exit source points loop if four valid points have been returned
            break
        else:
            border = [None] * 4  # Border thickness
            while True:
                border[0] = is_int(input('Insert left border thickness in pixels: '))
                if border[0] is None or border[0] < 0:
                    print('Invalid input.')
                else:
                    break
            while True:
                border[1] = is_int(input('Insert top border thickness in pixels: '))
                if border[1] is None or border[1] < 0:
                    print('Invalid input.')
                else:
                    break
            while True:
                border[2] = is_int(input('Insert right border thickness in pixels: '))
                if border[2] is None or border[2] < 0:
                    print('Invalid input.')
                else:
                    break
            while True:
                border[3] = is_int(input('Insert bottom border thickness in pixels: '))
                if border[3] is None or border[3] < 0:
                    print('Invalid input.')
                else:
                    break

            print('')
            img_src_b = cv2.copyMakeBorder(img_src, border[1], border[3], border[0], border[2], cv2.BORDER_CONSTANT)  # Add border to image (for planes outside image)

    return pts_src


def warp(img_src, ratio, show=False):

    while True:

        ans = input('Would you like to load an existing overlay (L),\n'
                    'create a new one by clicking on the image (M),\n'
                    'or insert source pixels by hand (N)?\n'
                    '\n'
                    '(press the specified key or ESC to exit) ')
        print('')

        if ans is 'l' or ans is 'L':
            # TODO Insert load code here
            pts_src = get_click_src(img_src)  # TODO Delete
            break
        elif ans is 'm' or ans is 'M':
            pts_src = get_click_src(img_src)
            break
        elif ans is 'n' or ans is 'N':
            # TODO Insert get points here
            pts_src = get_click_src(img_src)  # TODO Delete
            break


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

    if img_dst.shape[0] > img_dst_width:  # Resize warped image window if its width is larger than the screen width
        y = int(img_dst.shape[1] / (img_dst.shape[0] / img_dst_width))
        img_dst = cv2.resize(img_dst, (img_dst_width, y))
    elif img_dst.shape[1] > img_dst_height:  # Resize warped image window if its height is larger than the screen height
        x = int(img_dst.shape[0] / (img_dst.shape[0] / img_dst_height))
        img_dst = cv2.resize(img_dst, (x, img_dst_height))

    # DISPLAY RESULT (default: False)
    if show:
        cv2.imshow('', img_dst)  # Display warped image
        k = cv2.waitKey(0)
        if k == 27:  # ESC
            print('Exiting program...')
            sys.exit()  # Exit the whole program

    return img_dst

