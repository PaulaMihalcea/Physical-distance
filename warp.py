import cv2
import numpy as np
from get_dst_dim import get_dst_dim
from screeninfo import get_monitors
from utils import get_pts


def warp(img_src, ratio, show=False):

    pts_src = []  # Source points

    # BORDERS
    ans = input('Would you like to add a border? (Y/N) ')  # Ask the user if borders are needed

    while True:  # Wait for four valid source points
        while True:  # Wait for user input

            if ans is 'y' or ans is 'Y' or pts_src is None:  # Borders needed
                print('')
                border = [int(input('Insert left border thickness in pixels: ')), int(input('Insert top border thickness in pixels: ')), int(input('Insert right border thickness in pixels: ')), int(input('Insert bottom border thickness in pixels: '))]  # Get border thickness
                print('')
                img_src_b = cv2.copyMakeBorder(img_src, border[1], border[3], border[0], border[2], cv2.BORDER_CONSTANT)  # Add border to image (for planes outside image)
                break  # Exit input loop

            elif ans is 'n' or ans is 'N':  # No borders needed
                img_src_b = img_src.copy()
                break  # Exit input loop

            else:  # Wrong input; keep waiting for input
                ans = input('Invalid answer. Try again (Y/N): ')

        print('')
        print('Click on the four points of the floor plane (top left, top right, bottom right, bottom left) then press ENTER,\n'
              'or press SPACEBAR to go back and add or change borders.\n'
              'Otherwise, press ESC to exit.')
        print('')

        pts_src = get_pts(img_src_b)

        if pts_src is not None:  # Exit source points loop if four valid points have been returned
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

    # Display result (default: False)
    if show:
        cv2.imshow('', img_dst)  # Display warped image
        cv2.waitKey(0)

    return img_dst

