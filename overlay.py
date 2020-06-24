import cv2
import sys


def generate_overlay(img_dst, img_src, overlay_position=3, overlay_height=100):

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

    return img_src, overlay_position, (overlay_width + border_thickness * 2, overlay_height + border_thickness * 2), start_point, end_point


def apply_overlay(img_dst, img_src, overlay_position, overlay_dim, start_point, end_point):

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

    # OVERLAY CREATION: STATUS BAR
    if overlay_position == 0:  # Top left
        img_dst = cv2.rectangle(img_dst, (end_point[0], 0), (img_dst.shape[1] - 1, end_point[1] - 1), (128, 128, 128, 255), -1)  # Rectangle
        img_dst = cv2.line(img_dst, (end_point[0], 0), (end_point[0], end_point[1] - 1), (190, 190, 190, 255))  # Left border
        img_dst = cv2.line(img_dst, (end_point[0], 0), (img_dst.shape[1] - 1, 0), (190, 190, 190, 255))  # Top border
        img_dst = cv2.line(img_dst, (end_point[0], end_point[1] - 1), (img_dst.shape[1] - 1, end_point[1] - 1), (64, 64, 64, 255))  # Right border
        img_dst = cv2.line(img_dst, (img_dst.shape[1] - 1, 0), (img_dst.shape[1] - 1, end_point[1] - 1), (64, 64, 64, 255))  # Bottom border
    elif overlay_position == 1:  # Top right
        img_dst = cv2.rectangle(img_dst, (0, 0), (start_point[0] - 1, end_point[1] - 1), (128, 128, 128, 255), -1)  # Rectangle
        img_dst = cv2.line(img_dst, (0, 0), (0, end_point[1] - 1), (190, 190, 190, 255))  # Left border
        img_dst = cv2.line(img_dst, (0, 0), (start_point[0] - 1, 0), (190, 190, 190, 255))  # Top border
        img_dst = cv2.line(img_dst, (start_point[0] - 1, 0), (start_point[0] - 1, end_point[1] - 1), (64, 64, 64, 255))  # Right border
        img_dst = cv2.line(img_dst, (0, end_point[1] - 1), (start_point[0] - 1, end_point[1] - 1), (64, 64, 64, 255))  # Bottom border
    elif overlay_position == 2:  # Bottom right
        img_dst = cv2.rectangle(img_dst, (0, start_point[1]), (start_point[0] - 1, img_dst.shape[0] - 1), (128, 128, 128, 255), -1)  # Rectangle
        img_dst = cv2.line(img_dst, (0, start_point[1]), (0, img_dst.shape[0] - 1), (190, 190, 190, 255))  # Left border
        img_dst = cv2.line(img_dst, (0, start_point[1]), (start_point[0] - 1, start_point[1]), (190, 190, 190, 255))  # Top border
        img_dst = cv2.line(img_dst, (start_point[0] - 1, start_point[1]), (start_point[0] - 1, img_dst.shape[0] - 1), (64, 64, 64, 255))  # Right border
        img_dst = cv2.line(img_dst, (0, img_dst.shape[0] - 1), (start_point[0] - 1, img_dst.shape[0] - 1), (64, 64, 64, 255))  # Bottom border
    elif overlay_position == 3:  # Bottom left
        img_dst = cv2.rectangle(img_dst, (end_point[0], start_point[1]), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (128, 128, 128, 255), -1)  # Rectangle
        img_dst = cv2.line(img_dst, (end_point[0], start_point[1]), (end_point[0], img_dst.shape[0] - 1), (190, 190, 190, 255))  # Left border
        img_dst = cv2.line(img_dst, (end_point[0], start_point[1]), (img_dst.shape[1] - 1, start_point[1]), (190, 190, 190, 255))  # Top border
        img_dst = cv2.line(img_dst, (img_dst.shape[1] - 1, start_point[1]), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (64, 64, 64, 255))  # Right border
        img_dst = cv2.line(img_dst, (end_point[0], img_dst.shape[0] - 1), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (64, 64, 64, 255))  # Bottom border

    return img_dst
