import cv2
import sys


def generate_overlay(img_dst, img_src, overlay_position=3, overlay_height=100):

    # Overlay and source image size check
    if overlay_height > img_dst.shape[0]:  # Check if the overlay height is equal or smaller than the destination image height
        print('Overlay height exceeds destination image height. Overlay will be scaled to image height.')
        overlay_height = img_dst.shape[0]  # Resize overlay height accordingly

    if img_src.shape[0] != overlay_height:  # Check if the height of the image to be overlayed is different from the specified height of the overlay
        dim = (int((overlay_height / img_src.shape[0]) * img_src.shape[1]), overlay_height)
        img_src = cv2.resize(img_src, dim)  # Resize source image accordingly

    if img_src.shape[1] > img_dst.shape[1]:  # Check if the overlay width is equal or smaller than the destination image width
        print('Overlay width exceeds destination image width. Overlay will be scaled to image width.')
        overlay_width = img_dst.shape[1]
        dim = (overlay_width, int((overlay_width / img_dst.shape[1]) * img_src.shape[0]))
        img_src = cv2.resize(img_src, dim)  # Resize source image accordingly

        overlay_width = img_src.shape[1]
        overlay_height = img_src.shape[0]

    # Overlay position
    if overlay_position == 0:  # Top left
        start_point = (0, 0)
        end_point = (overlay_width, overlay_height)
    elif overlay_position == 1:  # Top right
        start_point = (img_dst.shape[1] - overlay_width, 0)
        end_point = (img_dst.shape[1], overlay_height)
    elif overlay_position == 2:  # Bottom right
        start_point = (img_dst.shape[1] - overlay_width, img_dst.shape[0] - overlay_height)
        end_point = (img_dst.shape[1], img_dst.shape[0])
    elif overlay_position == 3:  # Bottom left
        start_point = (0, img_dst.shape[0] - overlay_height)
        end_point = (overlay_width, img_dst.shape[0])
    else:
        print('Invalid position.')
        sys.exit(-1)

    return img_src, (overlay_width, overlay_height), start_point, end_point


def apply_overlay(img_dst, img_src, overlay_dim, start_point, end_point):

    # Parameters
    overlay_width = overlay_dim[0]
    overlay_height = overlay_dim[1]

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

    return img_dst
