import cv2
import sys
from warp import warp
from configparser import ConfigParser
from adjust_position import adjust_position


def generate_overlay(img_dst, pts_src, pts_dst, dst_dim=[]):

    # Setup
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    ratio = f.getfloat('General', 'ratio')

    status_bar_min_width = f.getint('Overlay', 'status_bar_min_width')  # Minimum status bar width
    status_bar_min_height = f.getint('Overlay', 'status_bar_min_height')  # Minimum status bar height

    overlay_max_width = img_dst.shape[1] - status_bar_min_width  # Maximum overlay width (status bar dependent)
    overlay_max_height = int(img_dst.shape[0] / 100 * f.getint('Overlay', 'overlay_max_height'))  # Maximum overlay height (percentage (!) of frame height)

    border_thickness = f.getint('Overlay', 'border_thickness')  # Overlay border thickness in pixels
    overlay_position = f.getint('Overlay', 'overlay_position')  # Overlay position on the video (0: top left; 1: top right; 2: bottom right; 3: bottom left)

    hor_offset = f.getint('Overlay', 'hor_offset')  # Manual horizontal offset (for people representation)
    ver_offset = f.getint('Overlay', 'ver_offset')  # Manual vertical offset (for people representation)

    position_tolerance = f.getint('Overlay', 'position_tolerance')

    overlay_colors = {'status_bar_background': tuple(map(int, f.get('Status bar colors', 'status_bar_background').split(', '))),
                      'overlay_left_top_border': tuple(map(int, f.get('Status bar colors', 'overlay_left_top_border').split(', '))),
                      'overlay_right_bottom_border': tuple(map(int, f.get('Status bar colors', 'overlay_right_bottom_border').split(', ')))
                      }

    if overlay_position != 0 and overlay_position != 1 and overlay_position != 2 and overlay_position != 3:  # Check overlay position validity
        print('Invalid overlay position.')
        sys.exit(-1)

    # Source image generation
    img_src, h = warp(img_dst, ratio, pts_src, pts_dst, dst_dim)  # Generate overlay source image
    src_width = img_src.shape[1]  # Overlay source original width
    src_height = img_src.shape[0]  # Overlay source original height

    # Overlay size check
    if img_src.shape[1] + border_thickness * 2 > overlay_max_width:  # Check if overlay width is too large
        new_width = overlay_max_width - border_thickness * 2
        new_height = int(overlay_max_width / img_src.shape[1] * img_src.shape[0])
        if new_width == 0:
            new_width = 1
        elif new_height == 0:
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize overlay width accordingly

    if img_src.shape[0] + border_thickness * 2 > overlay_max_height:  # Check if overlay height is too large
        new_height = overlay_max_height
        new_width = int(overlay_max_height / img_src.shape[0] * img_src.shape[1])
        if new_width == 0:
            new_width = 1
        elif new_height == 0:
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize overlay width accordingly

    # Overlay background
    if img_src.shape[0] < status_bar_min_height:  # Add empty background to overlay if it's too small with respect to the status bar
        offset = int((status_bar_min_height - (img_src.shape[0] + border_thickness * 2 - 2)) / 2) - 1
        if offset < 0:
            offset = 0
        if (status_bar_min_height - (img_src.shape[0] + border_thickness * 2 - 1)) % 2 == 0:
            img_src = cv2.copyMakeBorder(img_src, offset + 1, offset + 1, 0, 0, cv2.BORDER_CONSTANT, value=overlay_colors['status_bar_background'])
        else:
            img_src = cv2.copyMakeBorder(img_src, offset, offset + 1, 0, 0, cv2.BORDER_CONSTANT, value=overlay_colors['status_bar_background'])
        ver_offset += int(offset / 2)
    else:
        offset = 0

    # Overlay border creation
    img_src = cv2.copyMakeBorder(img_src, border_thickness, 0, border_thickness, 0, cv2.BORDER_CONSTANT, value=overlay_colors['overlay_left_top_border'])
    img_src = cv2.copyMakeBorder(img_src, 0, border_thickness, 0, border_thickness, cv2.BORDER_CONSTANT, value=overlay_colors['overlay_right_bottom_border'])

    overlay_width = img_src.shape[1]
    overlay_height = img_src.shape[0]

    # Overlay position
    corners = []
    if overlay_position == 0:  # Top left
        start_point = [0, 0]
        end_point = [overlay_width, overlay_height]
        corners.extend([(end_point[0], 0), (img_dst.shape[1] - 1, 0), (img_dst.shape[1] - 1, status_bar_min_height), (end_point[0], status_bar_min_height)])
    elif overlay_position == 1:  # Top right
        start_point = [img_dst.shape[1] - overlay_width, 0]
        end_point = [img_dst.shape[1], overlay_height]
        corners.extend([(0, 0), (start_point[0] - 1, 0), (start_point[0] - 1, status_bar_min_height), (0, status_bar_min_height)])
    elif overlay_position == 2:  # Bottom right
        start_point = [img_dst.shape[1] - overlay_width, img_dst.shape[0] - overlay_height]
        end_point = [img_dst.shape[1], img_dst.shape[0]]
        corners.extend([(0, start_point[1] - status_bar_min_height + overlay_height - 1), (start_point[0] - 1, start_point[1] - status_bar_min_height + overlay_height - 1), (start_point[0] - 1, img_dst.shape[0] - 1), (0, img_dst.shape[0] - 1)])
    elif overlay_position == 3:  # Bottom left
        start_point = (0, img_dst.shape[0] - overlay_height)
        end_point = (overlay_width, img_dst.shape[0])
        corners.extend([(end_point[0], start_point[1] - status_bar_min_height + overlay_height - 1), (img_dst.shape[1] - 1, start_point[1] - status_bar_min_height + overlay_height - 1), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (end_point[0], img_dst.shape[0] - 1)])

    width_ratio = src_width / img_src.shape[1]
    height_ratio = src_height / img_src.shape[0]

    overlay_data = {'img_src': img_src,
                    'overlay_position': overlay_position,
                    'overlay_dim': [overlay_width, overlay_height],
                    'overlay_colors': overlay_colors,
                    'start_end_points': [start_point, end_point],
                    'corners': corners,
                    'h': h,
                    'width_height_ratio': [width_ratio, height_ratio],
                    'offset': [hor_offset, ver_offset],
                    'border_thickness': border_thickness,
                    'map_offset': offset,
                    'position_tolerance': position_tolerance
                    }

    return overlay_data


def apply_overlay(img_dst, overlay_data, people, status=[]):

    # Parameters
    img_src = overlay_data['img_src']
    border_thickness = overlay_data['border_thickness']
    overlay_width = overlay_data['overlay_dim'][0] + border_thickness * 2
    overlay_height = overlay_data['overlay_dim'][1] + border_thickness * 2
    overlay_colors = overlay_data['overlay_colors']
    start_point = overlay_data['start_end_points'][0]
    end_point = overlay_data['start_end_points'][1]
    corners = overlay_data['corners']
    hor_offset = overlay_data['offset'][0]
    ver_offset = overlay_data['offset'][1]
    map_offset = overlay_data['map_offset']
    position_tolerance = overlay_data['position_tolerance']

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
    img_dst = cv2.rectangle(img_dst, corners[0], corners[2], overlay_colors['status_bar_background'], -1)  # Rectangle
    img_dst = cv2.line(img_dst, corners[0], corners[3], overlay_colors['overlay_left_top_border'])  # Left border
    img_dst = cv2.line(img_dst, corners[0], corners[1], overlay_colors['overlay_left_top_border'])  # Top border
    img_dst = cv2.line(img_dst, corners[1], corners[2], overlay_colors['overlay_right_bottom_border'])  # Right border
    img_dst = cv2.line(img_dst, corners[3], corners[2], overlay_colors['overlay_right_bottom_border'])  # Bottom border

    # Adjust people position (if outside map)
    if people[0] is not None:
        add_x = start_point[0] + border_thickness + hor_offset
        add_y = start_point[1] + border_thickness + ver_offset
        dim_x = [start_point[0] + border_thickness + hor_offset, end_point[0] - border_thickness + hor_offset]
        dim_y = [start_point[1] + border_thickness + ver_offset + map_offset, end_point[1] - border_thickness + ver_offset - map_offset * 2]

        people[0] = adjust_position(people[0], (add_x, add_y), dim_x, dim_y, position_tolerance)

    if people[0] is not None and len(people[0]) > 1:
        # People positions (single color version)
        for k in range(0, len(people[0])):
            img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 255, 255, 255), -1)

        # People positions (multi color version)
        v = people[1]  # People that do not respect minimum distance
        for k in range(0, len(people[0])):
            img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 255, 0, 255), -1)
            for l in range(0, len(v)):
                if l == k:
                    img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 0, 255, 255), -1)
        n_people = str(len(people[0]))

    elif people[0] is not None and len(people[0]) == 1:
        # People positions (single color version)
        for k in range(0, len(people[0])):
            img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 255, 0, 255), -1)
        n_people = str(1)
    else:
        n_people = str(0)

    # Status bar text
    img_dst = cv2.putText(img_dst, status[0][0] + ' ' + n_people, (corners[0][0] + status[0][2] - 1, corners[0][1] + status[0][3]), cv2.FONT_HERSHEY_DUPLEX, 0.6, status[0][1], 1)  # First line
    img_dst = cv2.putText(img_dst, status[1][0], (corners[0][0] + status[1][2] - 1, corners[0][1] + status[1][3]), cv2.FONT_HERSHEY_DUPLEX, 0.6, status[1][1], 1)  # Second line
    img_dst = cv2.putText(img_dst, status[2][0], (corners[0][0] + status[2][2] - 1, corners[0][1] + status[2][3]), cv2.FONT_HERSHEY_DUPLEX, 0.6, status[2][1], 1)  # Third line

    return img_dst
