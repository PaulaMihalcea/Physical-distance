import sys
import cv2
import numpy as np
from configparser import ConfigParser
from screeninfo import get_monitors
from get_dst_dim import get_dst_dim


def warp(img_src, pts_src, pts_dst, dst_dim, show=False):

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


def warp_c(img_src, show=False):

    # Setup
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    chessboard_length_cm = f.getfloat('Chessboard', 'chessboard_length') * 100

    roi_x_cm = f.getfloat('Chessboard', 'roi_x') * 100
    roi_y_cm = f.getfloat('Chessboard', 'roi_y') * 100

    pts_src_ini = f.get('Chessboard', 'chessboard_src')  # Source points (for warp)
    if pts_src_ini == 'None':
        pts_src = None
    else:
        pts_src = []
        pts_src_ini = pts_src_ini.split('\n')
        for i in range(0, len(pts_src_ini)):
            pts_src.append([int(pts_src_ini[i].split(' ')[0]), int(pts_src_ini[i].split(' ')[1])])
        pts_src = np.array(pts_src)  # TODO float32 array
        print('Chessboard reference points have been found.')

    # Chessboard length in pixels
    dst_dim = get_dst_dim(pts_src)

    if dst_dim[0] > dst_dim[1]:
        chessboard_length_px = dst_dim[0] - 1
    else:
        chessboard_length_px = dst_dim[1] - 1

    pts_dst = np.array([[0, 0], [chessboard_length_px, 0], [chessboard_length_px, chessboard_length_px], [0, chessboard_length_px]])

    # Homography
    h, _ = cv2.findHomography(pts_src, pts_dst)

    src_width = img_src.shape[1]
    src_height = img_src.shape[0]

    x_translation = src_width * 10
    y_translation = src_height * 10

    t = np.array([[1, 0, x_translation],
                  [0, 1, y_translation],
                  [0, 0, 1]], dtype='float32')

    th = np.dot(t, h)

    dst_width = int(th[0][2]) * 10
    dst_height = int(th[1][2]) * 10

    img_dst = cv2.warpPerspective(img_src, th, (dst_width, dst_height), borderValue=(255, 0, 0, 255))  # TODO Change background color to black

    # Cropping
    roi_x_px = int(chessboard_length_px * roi_x_cm / chessboard_length_cm)
    roi_y_px = int(chessboard_length_px * roi_y_cm / chessboard_length_cm)

    img_dst = img_dst[y_translation - roi_y_px: y_translation + chessboard_length_px + roi_y_px, x_translation - roi_x_px: x_translation + chessboard_length_px + roi_x_px]

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
        y_translation = int(img_dst.shape[0] / (img_dst.shape[1] / img_dst_width))
        img_dst = cv2.resize(img_dst, (img_dst_width, y_translation))
    elif img_dst.shape[0] > img_dst_height:  # Resize warped image window if its height is larger than the screen height
        x_translation = int(img_dst.shape[1] / (img_dst.shape[0] / img_dst_height))
        img_dst = cv2.resize(img_dst, (x_translation, img_dst_height))

    # Show warped image (default: False)
    if show:
        cv2.imshow('', img_dst)  # Display warped image
        k = cv2.waitKey(0)
        if k == 27:  # ESC
            print('Exiting program...')
            sys.exit()  # Exit program

    return img_dst, th, (x_translation - roi_x_px, y_translation - roi_y_px), (roi_x_cm * 2 + chessboard_length_cm, roi_y_cm * 2 + chessboard_length_cm)
