import cv2
import sys
import numpy as np
import random
from warp import warp


def generate_overlay(img_dst, overlay_position=3, overlay_height=100):

    # SOURCE IMAGE GENERATION
    img_src, h = warp(img_dst, 1)  # Generate overlay source image
    src_width = img_src.shape[1]  # Overlay source original width
    src_height = img_src.shape[0]  # Overlay source original height

    # OVERLAY PARAMETERS
    border_thickness = 1  # Overlay border thickness in pixels
    if overlay_position != 0 and overlay_position != 1 and overlay_position != 2 and overlay_position != 3:  # Check overlay position validity
        print('Invalid overlay position.')
        sys.exit(-1)

    # OVERLAY SIZE CHECK
    '''
    if img_src.shape[0] != overlay_height:  # Check if the height of the image to be overlayed is different from the specified height of the overlay
        dim = (int((overlay_height / img_src.shape[0]) * img_src.shape[1]), overlay_height)
        img_src = cv2.resize(img_src, dim)  # Resize source image accordingly

    if img_src.shape[1] + border_thickness * 2 > img_dst.shape[1]:  # Check if the overlay width is larger than the destination image width
        print('Overlay width exceeds destination image width. Overlay will be scaled accordingly.')
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
    '''

    overlay_width = int(overlay_height / (src_width / src_height))

    if img_src.shape[0] + border_thickness * 2 > overlay_height:  # Check if the overlay height is too large
        new_width = int(overlay_height / img_src.shape[0] * img_src.shape[1])
        new_height = overlay_height - border_thickness * 2
        if new_width == 0:
            new_width = 1
        elif new_height == 0:
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize overlay height accordingly

    if img_src.shape[1] + border_thickness * 2 > overlay_width:  # Check if the overlay width is too large
        new_width = overlay_width - border_thickness * 2
        new_height = int(overlay_width / img_src.shape[1] * img_src.shape[0])
        if new_width == 0:
            new_width = 1
        elif new_height == 0:
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize overlay width accordingly


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

    width_ratio = src_width / img_src.shape[1]
    height_ratio = src_height / img_src.shape[0]

    return img_src, overlay_position, (overlay_width + border_thickness * 2, overlay_height + border_thickness * 2), start_point, end_point, corners, h, (width_ratio, height_ratio)


def apply_overlay(img_dst, img_src, overlay_position, overlay_dim, start_point, end_point, corners, points=None, status_1='', status_2='', status_3=''):

    # PARAMETERS
    overlay_width = overlay_dim[0]
    overlay_height = overlay_dim[1]

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

    # POINTS
    if points is not None:
        for i in range(0, len(points)):
            img_dst = cv2.circle(img_dst, (start_point[0] + points[i][0], start_point[1] + points[i][1]), 3, (random.randint(150, 256), random.randint(150, 256), random.randint(150, 256), 255), -1)

    return img_dst
