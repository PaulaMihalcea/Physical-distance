import cv2
import sys
import numpy as np
from warp import warp


def apply_overlay(img_dst, points, overlay_position=3, overlay_height=100, pts_src=[], status_1='', status_2='', status_3='', first=False):

    img_src, pts_src = warp(img_dst, 1, pts_src, points, first=first)  # Generate overlay source image  # TODO warp(cv2.imread('test/stone.jpg'), 1)

    # OVERLAY PARAMETERS
    border_thickness = 1  # Overlay border thickness in pixels
    if overlay_position != 0 and overlay_position != 1 and overlay_position != 2 and overlay_position != 3:  # Check overlay position validity
        print('Invalid overlay position.')
        sys.exit(-1)

    # OVERLAY AND SOURCE IMAGE SIZE CHECK
    if img_src.shape[0] != overlay_height:  # Check if the height of the image to be overlayed is different from the specified height of the overlay
        dim = (int((overlay_height / img_src.shape[0]) * img_src.shape[1]), overlay_height)
        img_src = cv2.resize(img_src, dim)  # Resize source image accordingly

    if img_src.shape[1] + border_thickness * 2 > img_dst.shape[1]:  # Check if the overlay width is larger than the destination image width
        print('Overlay width exceeds destination image width. Overlay will be scaled to image width.')
        overlay_width = img_dst.shape[1] - border_thickness * 2
        overlay_height = int(overlay_width / img_src.shape[1] * img_src.shape[0])
        dim = (overlay_width, overlay_height)
        img_src = cv2.resize(img_src, dim)   # Resize overlay width accordingly

    if img_src.shape[0] + border_thickness * 2 > img_dst.shape[0]:  # Check if the overlay height is larger than the destination image height
        print('Overlay height exceeds destination image height. Overlay will be scaled to image height.')
        overlay_height = img_dst.shape[0] - border_thickness * 2
        overlay_width = int(overlay_height / img_src.shape[0] * img_src.shape[1])
        dim = (overlay_width, overlay_height)
        img_src = cv2.resize(img_src, dim)   # Resize overlay height accordingly

    overlay_width = img_src.shape[1] + border_thickness * 2
    overlay_height = img_src.shape[0] + border_thickness * 2

    # OVERLAY BORDER CREATION
    img_src = cv2.copyMakeBorder(img_src, border_thickness, 0, border_thickness, 0, cv2.BORDER_CONSTANT, value=(190, 190, 190, 255))
    img_src = cv2.copyMakeBorder(img_src, 0, border_thickness, 0, border_thickness, cv2.BORDER_CONSTANT, value=(64, 64, 64, 255))

    # OVERLAY POSITION
    corners = []
    if overlay_position == 0:  # Top left
        start_point = (0, 0)
        end_point = (overlay_width, overlay_height)
        corners.extend([(end_point[0], 0), (img_dst.shape[1] - 1, 0), (img_dst.shape[1] - 1, end_point[1] - 1), (end_point[0], end_point[1] - 1)])
    elif overlay_position == 1:  # Top right
        start_point = (img_dst.shape[1] - overlay_width, 0)
        end_point = (img_dst.shape[1], overlay_height)
        corners.extend([(0, 0), (start_point[0] - 1, 0), (start_point[0] - 1, end_point[1] - 1), (0, end_point[1] - 1)])
    elif overlay_position == 2:  # Bottom right
        start_point = (img_dst.shape[1] - overlay_width, img_dst.shape[0] - overlay_height)
        end_point = (img_dst.shape[1], img_dst.shape[0])
        corners.extend([(0, start_point[1]), (start_point[0] - 1, start_point[1]), (start_point[0] - 1, img_dst.shape[0] - 1), (0, img_dst.shape[0] - 1)])
    elif overlay_position == 3:  # Bottom left
        start_point = (0, img_dst.shape[0] - overlay_height)
        end_point = (overlay_width, img_dst.shape[0])
        corners.extend([(end_point[0], start_point[1]), (img_dst.shape[1] - 1, start_point[1]), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (end_point[0], img_dst.shape[0] - 1)])


    ###### ACTUAL OVERLAY DRAWING

    # PARAMETERS
    overlay_width = overlay_width + border_thickness * 2
    overlay_height = overlay_height + border_thickness * 2

    # OVERLAY CREATION: IMAGE
    i = start_point[0]
    io = 0

    while i < end_point[0] and io <= overlay_width:
        j = start_point[1]
        jo = 0
        while j < end_point[1] and jo <= overlay_height:
            img_dst[j][i] = img_src[jo][io]
            j += 1
            jo += 1
        i += 1
        io += 1

    # STATUS BAR
    img_dst = cv2.rectangle(img_dst, corners[0], corners[2], (128, 128, 128, 255), -1)  # Rectangle
    img_dst = cv2.line(img_dst, corners[0], corners[3], (190, 190, 190, 255))  # Left border
    img_dst = cv2.line(img_dst, corners[0], corners[1], (190, 190, 190, 255))  # Top border
    img_dst = cv2.line(img_dst, corners[1], corners[2], (64, 64, 64, 255))  # Right border
    img_dst = cv2.line(img_dst, corners[3], corners[2], (64, 64, 64, 255))  # Bottom border

    # STATUS BAR TEXT
    img_dst = cv2.putText(img_dst, status_1[0], (corners[0][0] + 5, corners[0][1] + 19), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_1[1], 1)  # First line
    img_dst = cv2.putText(img_dst, status_2[0], (corners[0][0] + 5, corners[0][1] + 46), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_2[1], 1)  # Second line
    img_dst = cv2.putText(img_dst, status_3[0], (corners[0][0] + 5, corners[0][1] + 72), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_3[1], 1)  # Third line

    return img_dst, pts_src
