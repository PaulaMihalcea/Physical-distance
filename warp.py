import sys
import cv2
from screeninfo import get_monitors


def warp(img_src, ratio, pts_src, pts_dst, dst_dim, show=False):

    # Warp
    dst_width = dst_dim[0]  # TODO rimuovi (anche dalla signature)
    dst_height = dst_dim[1]  # TODO rimuovi (anche dalla signature)

    h, _ = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    img_dst = cv2.warpPerspective(img_src, h, (dst_width, dst_height))  # Warp source image based on homography

    # Display resolution check
    disp = []  # Monitor info list

    for m in get_monitors():  # Cycle on monitors found by the screeninfo library
        info = str(m)
        disp_w = int(info[info.find('width='):info.find(', h')][6:])
        disp_h = int(info[info.find('height='):info.find(', width_mm=')][7:])
        name = info[info.find('name='):info.find(')')][5:].replace('\'', '')  # Get monitor name
        disp.append((disp_w, disp_h, name))

    for i in range(0, len(disp)):  # Get width and height of main monitor; it is assumed to be the first that appears in the list
        if disp[i][2] == 'DISPLAY1':
            j = i
        elif disp[i][2] == 'DVI-D-0':
            j = i
        elif disp[i][2] == 'HDMI-0':
            j = i

    disp_width = disp[j][0]
    disp_height = disp[j][1]

    disp_tolerance = 50  # If the warped image is too large, an amount of pixels equal to this number will be left around the image window, so as to avoid occupying the whole screen
    img_dst_width = disp_width - disp_tolerance
    img_dst_height = disp_height - disp_tolerance

    if img_dst.shape[1] > img_dst_width:  # Resize warped image window if its width is larger than the screen width
        y = int(img_dst.shape[0] / (img_dst.shape[1] / img_dst_width))
        img_dst = cv2.resize(img_dst, (img_dst_width, y))
    elif img_dst.shape[0] > img_dst_height:  # Resize warped image window if its height is larger than the screen height
        x = int(img_dst.shape[1] / (img_dst.shape[0] / img_dst_height))
        img_dst = cv2.resize(img_dst, (x, img_dst_height))

    # Show warped image (default: False)
    if show:
        cv2.imshow('', img_dst)  # Display warped image
        k = cv2.waitKey(0)
        if k == 27:  # ESC
            print('Exiting program...')
            sys.exit()  # Exit program

    return img_dst, h
