import cv2
import sys
from warp import warp
from configparser import ConfigParser


def generate_overlay(img_dst, pts_src):

    # Setup
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    overlay_max_width = f.getint('Overlay', 'overlay_max_width')  # Maximum overlay width
    overlay_max_height = f.getint('Overlay', 'overlay_max_height')  # Maximum overlay height

    border_thickness = f.getint('Overlay', 'border_thickness')  # Overlay border thickness in pixels
    overlay_position = f.getint('Overlay', 'overlay_position')  # Overlay position on the video (0: top left; 1: top right; 2: bottom right; 3: bottom left)

    overlay_colors = {'status_bar_background': tuple(map(int, f.get('Status bar colors', 'status_bar_background').split(', '))),
                      'overlay_left_top_border': tuple(map(int, f.get('Status bar colors', 'overlay_left_top_border').split(', '))),
                      'overlay_right_bottom_border': tuple(map(int, f.get('Status bar colors', 'overlay_right_bottom_border').split(', ')))
                      }

    if overlay_position != 0 and overlay_position != 1 and overlay_position != 2 and overlay_position != 3:  # Check overlay position validity
        print('Invalid overlay position.')
        sys.exit(-1)

    # Source image generation
    img_src, h = warp(img_dst, 1, pts_src)  # Generate overlay source image
    src_width = img_src.shape[1]  # Overlay source original width
    src_height = img_src.shape[0]  # Overlay source original height

    # Overlay size check
    overlay_width = overlay_max_width
    overlay_height = int(overlay_width / (src_width / src_height))
    print('overlay width, overlay height:', overlay_width, overlay_height)
    scaled = False

    if img_src.shape[1] + border_thickness * 2 > overlay_width:  # Check if the overlay width is too large
        new_width = overlay_width - border_thickness * 2
        new_height = int(overlay_width / img_src.shape[1] * img_src.shape[0])
        if new_width == 0:
            new_width = 1
        elif new_height == 0:
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize overlay width accordingly
        print('scaled on width')
        scaled = True

    if img_src.shape[0] + border_thickness * 2 > img_dst.shape[0] and scaled:  # Check if the overlay height is too large
        new_width = int(overlay_height / img_src.shape[0] * img_src.shape[1])
        new_height = img_dst.shape[0] - border_thickness * 2
        if new_width == 0:
            new_width = 1
        elif new_height == 0:
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize overlay height accordingly
        print('scaled on height')





    overlay_width = img_src.shape[1] + border_thickness * 2
    overlay_height = img_src.shape[0] + border_thickness * 2

    # Overlay border creation
    img_src = cv2.copyMakeBorder(img_src, border_thickness, 0, border_thickness, 0, cv2.BORDER_CONSTANT, value=overlay_colors['overlay_left_top_border'])
    img_src = cv2.copyMakeBorder(img_src, 0, border_thickness, 0, border_thickness, cv2.BORDER_CONSTANT, value=overlay_colors['overlay_right_bottom_border'])

    # Overlay position
    corners = []
    if overlay_position == 0:  # Top left
        start_point = [0, 0]
        end_point = [overlay_width, overlay_height]
        corners.extend([(end_point[0], 0), (img_dst.shape[1] - 1, 0), (img_dst.shape[1] - 1, end_point[1] - 1), (end_point[0], end_point[1] - 1)])
        print(corners)
    elif overlay_position == 1:  # Top right
        start_point = [img_dst.shape[1] - overlay_width, 0]
        end_point = [img_dst.shape[1], overlay_height]
        corners.extend([(0, 0), (start_point[0] - 1, 0), (start_point[0] - 1, end_point[1] - 1), (0, end_point[1] - 1)])
    elif overlay_position == 2:  # Bottom right
        start_point = [img_dst.shape[1] - overlay_width, img_dst.shape[0] - overlay_height]
        end_point = [img_dst.shape[1], img_dst.shape[0]]
        corners.extend([(0, start_point[1]), (start_point[0] - 1, start_point[1]), (start_point[0] - 1, img_dst.shape[0] - 1), (0, img_dst.shape[0] - 1)])
    elif overlay_position == 3:  # Bottom left
        start_point = [0, img_dst.shape[0] - overlay_height]
        end_point = [overlay_width, img_dst.shape[0]]
        print('start point, end point:', start_point, end_point)
        if (start_point[1] - end_point[1]) < 80:
            print('oh no la barra è troppo corta')
            start_point[1] = 80 - (start_point[1] - end_point[1])
            print('new start point:', start_point[1])
        corners.extend([(end_point[0], start_point[1]), (img_dst.shape[1] - 1, start_point[1]), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (end_point[0], img_dst.shape[0] - 1)])

    width_ratio = src_width / img_src.shape[1]
    height_ratio = src_height / img_src.shape[0]

    overlay_data = {'img_src': img_src,  # 0
                    'overlay_position': overlay_position,  # 1
                    'overlay_dim': [overlay_width + border_thickness * 2, overlay_height + border_thickness * 2],  # 2
                    'overlay_colors': overlay_colors,  # 3
                    'start_end_points': [start_point, end_point],  # 4
                    'corners': corners,  # 5
                    'h': h,  # 6
                    'width_height_ratio': [width_ratio, height_ratio]  # 7
                    }

    return overlay_data


def apply_overlay(img_dst, overlay_data, people=None, status=[]):

    # Parameters
    img_src = overlay_data['img_src']
    overlay_width = overlay_data['overlay_dim'][0]
    overlay_height = overlay_data['overlay_dim'][1]
    overlay_colors = overlay_data['overlay_colors']
    start_point = overlay_data['start_end_points'][0]
    end_point = overlay_data['start_end_points'][1]
    corners = overlay_data['corners']

    # Overlay image creation
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

    # Status bar background
    img_dst = cv2.rectangle(img_dst, corners[0], corners[2], overlay_colors[0], -1)  # Rectangle
    img_dst = cv2.line(img_dst, corners[0], corners[3], overlay_colors[1])  # Left border
    img_dst = cv2.line(img_dst, corners[0], corners[1], overlay_colors[1])  # Top border
    img_dst = cv2.line(img_dst, corners[1], corners[2], overlay_colors[2])  # Right border
    img_dst = cv2.line(img_dst, corners[3], corners[2], overlay_colors[2])  # Bottom border

    # Status bar text
    img_dst = cv2.putText(img_dst, status[0][0], (corners[0][0] + 4, corners[0][1] + 19), cv2.FONT_HERSHEY_DUPLEX, 0.6, status[0][1], 1)  # First line
    img_dst = cv2.putText(img_dst, status[1][0], (corners[0][0] + 4, corners[0][1] + 46), cv2.FONT_HERSHEY_DUPLEX, 0.6, status[1][1], 1)  # Second line
    img_dst = cv2.putText(img_dst, status[2][0], (corners[0][0] + 4, corners[0][1] + 72), cv2.FONT_HERSHEY_DUPLEX, 0.6, status[2][1], 1)  # Third line

    # People positions
    if people is not None:  # TODO prova a sostituire il default con [] (magari non serve l'if e non genera errore se len è zero)
        for i in range(0, len(people)):
            img_dst = cv2.circle(img_dst, (start_point[0] + people[i][0], start_point[1] + people[i][1]), 3, (0, 255, 0, 255), -1)

    return img_dst
