import sys
import cv2
import numpy as np
import inspect
from screeninfo import get_monitors
from get_points import get_dim


def warp(img_src, floor_data, mat_data, mode, show=False):

    # Floor mode
    if mode:
        # Get destination points
        if floor_data['floor_dst'] is None:
            dst_dim = get_dim(floor_data['floor_src'], mode, floor_data['ratio'])  # Calculate dimensions of destination image

            floor_data['floor_dst'] = np.array([[0, 0], [dst_dim[0] - 1, 0], [dst_dim[0] - 1, dst_dim[0] - 1], [0, dst_dim[0] - 1]])  # Set destination points
        else:
            dst_dim = get_dim(floor_data['floor_dst'], mode, floor_data['ratio'])  # Calculate dimensions of destination image

        # Warp
        h, _ = cv2.findHomography(floor_data['floor_src'], floor_data['floor_dst'])  # Calculate homography

        img_dst = cv2.warpPerspective(img_src, h, (dst_dim[0], dst_dim[1]))  # Warp source image based on homography

    # Mat mode
    elif not mode:

        # Get mat data
        mat_width_cm = mat_data['mat_width']
        mat_height_cm = mat_data['mat_height']

        roi_x_cm = mat_data['roi_x']
        roi_y_cm = mat_data['roi_y']

        mat_src = mat_data['mat_src']

        # Mat dimensions in pixels
        mat_length_px = get_dim(mat_src, mode)[0]

        mat_dst = np.array([[0, 0], [mat_length_px, 0], [mat_length_px, mat_length_px], [0, mat_length_px]])

        # Homography
        h, _ = cv2.findHomography(mat_src, mat_dst)

        src_width = img_src.shape[1]
        src_height = img_src.shape[0]

        # Homography translation
        x_translation = src_width * 10
        y_translation = src_height * 10

        t = np.array([[1, 0, x_translation],
                      [0, 1, y_translation],
                      [0, 0, 1]], dtype='float32')

        th = np.dot(t, h)

        # Warp source image based on translated homography
        dst_width = int(th[0][2]) * 10
        dst_height = int(th[1][2]) * 10

        img_dst = cv2.warpPerspective(img_src, th, (dst_width, dst_height))

        # Cropping
        roi_x_px = int(mat_length_px * roi_x_cm / mat_width_cm)
        roi_y_px = int(mat_length_px * roi_y_cm / mat_height_cm)

        img_dst = img_dst[y_translation - roi_y_px: y_translation + mat_length_px + roi_y_px, x_translation - roi_x_px: x_translation + mat_length_px + roi_x_px]

    else:  # Shouldn't even get to this point, but whatever
        print('An error occurred in the ' + inspect.stack()[0][3] + ' function, exiting program.')
        sys.exit(-1)

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

    if mode:
        return img_dst, h, None, None

    elif not mode:
        return img_dst, th, (x_translation - roi_x_px, y_translation - roi_y_px), (roi_x_cm * 2 + mat_width_cm, roi_y_cm * 2 + mat_height_cm)
