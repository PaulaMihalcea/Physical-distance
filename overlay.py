import cv2
import sys


def overlay(img_src, img_dst, overlay_height, position, show=False):

    # Overlay and source image size check
    if overlay_height > img_dst.shape[0]:  # Check if the overlay height is equal or smaller than the destination image height
        print('Minimap height exceeds destination image height. Minimap will be scaled to image height.')
        overlay_height = img_dst.shape[0]  # Resize overlay height accordingly

    if img_src.shape[0] != overlay_height:  # Check if the height of the image to be overlayed is different from the specified height of the overlay
        dim = (int((overlay_height / img_src.shape[0]) * img_src.shape[1]), overlay_height)
        img_src = cv2.resize(img_src, dim)  # Resize source image accordingly

    overlay_width = img_src.shape[1]
    overlay_height = img_src.shape[0]

    if overlay_width > img_dst.shape[1]:  # Check if the overlay width is equal or smaller than the destination image width
        print('Minimap width exceeds destination image width. Minimap will be scaled to image width.')
        overlay_width = img_dst.shape[1]
        dim = (overlay_width, int((overlay_width / img_dst.shape[1]) * img_src.shape[0]))
        img_src = cv2.resize(img_src, dim)  # Resize source image accordingly

    # Overlay position
    if position == 0:  # Top left
        start_point = (0, 0)
        end_point = (overlay_width, overlay_height)
    elif position == 1:  # Top right
        start_point = (img_dst.shape[1] - overlay_width, 0)
        end_point = (img_dst.shape[1], overlay_height)
    elif position == 2:  # Bottom right
        start_point = (img_dst.shape[1] - overlay_width, img_dst.shape[0] - overlay_height)
        end_point = (img_dst.shape[1], img_dst.shape[0])
    elif position == 3:  # Bottom left
        start_point = (0, img_dst.shape[0] - overlay_height)
        end_point = (overlay_width, img_dst.shape[0])
    else:
        print('Invalid position.')
        sys.exit(-1)

    # Overlay creation
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

    # Show result (default: False)
    if show:
        cv2.imshow('Image with overlay', img_dst)
        cv2.waitKey(0)

    return img_dst
