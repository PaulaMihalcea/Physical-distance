import cv2
import sys
from warp import warp
from transform_coords import adjust_position


def generate_overlay(img_dst, floor_data, mat_data, status_bar_data, overlay_data, mode):

    # Setup
    overlay_max_width = img_dst.shape[1] - overlay_data['status_bar_min_width']  # Maximum overlay width (status bar dependent)
    overlay_max_height = int(img_dst.shape[0] / 100 * overlay_data['overlay_max_height'])  # Maximum overlay height (percentage (!) of frame height)

    if overlay_data['overlay_position'] != 0 and overlay_data['overlay_position'] != 1 and overlay_data['overlay_position'] != 2 and overlay_data['overlay_position'] != 3:  # Check overlay position validity
        print('Invalid overlay position.')
        sys.exit(-1)

    # Source image generation
    img_src, h, warp_offset, map_dim = warp(img_dst, floor_data, mat_data, mode)  # Generate map source image
    src_width = img_src.shape[1]  # Map source original width
    src_height = img_src.shape[0]  # Map source original height

    # Map size check
    if img_src.shape[1] + overlay_data['border_thickness'] * 2 > overlay_max_width:  # Check if map width is too large
        new_width = overlay_max_width - overlay_data['border_thickness'] * 2
        new_height = int(overlay_max_width / img_src.shape[1] * img_src.shape[0])
        if new_width == 0:  # In extreme cases might become 0, so 1 is the minimum
            new_width = 1
        elif new_height == 0:  # In extreme cases might become 0, so 1 is the minimum
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize map accordingly

    if img_src.shape[0] + overlay_data['border_thickness'] * 2 > overlay_max_height:  # Check if map height is too large
        new_height = overlay_max_height
        new_width = int(overlay_max_height / img_src.shape[0] * img_src.shape[1])
        if new_width == 0:  # In extreme cases might become 0, so 1 is the minimum
            new_width = 1
        elif new_height == 0:  # In extreme cases might become 0, so 1 is the minimum
            new_height = 1
        img_src = cv2.resize(img_src, (new_width, new_height))   # Resize map accordingly

    # Map background
    if img_src.shape[0] < overlay_data['status_bar_min_height']:  # Add empty background (= border) to map if it's too small with respect to the status bar
        offset = int((overlay_data['status_bar_min_height'] - (img_src.shape[0] + overlay_data['border_thickness'] * 2 - 2)) / 2) - 1  # An additional top border will introduce an offset that must be considered for a correct people position drawing
        if offset < 0:
            offset = 0
        if (overlay_data['status_bar_min_height'] - (img_src.shape[0] + overlay_data['border_thickness'] * 2 - 1)) % 2 == 0:  # Compute and add top and bottom border
            img_src = cv2.copyMakeBorder(img_src, offset + 1, offset + 1, 0, 0, cv2.BORDER_CONSTANT, value=status_bar_data['status_bar_background'])
        else:
            img_src = cv2.copyMakeBorder(img_src, offset, offset + 1, 0, 0, cv2.BORDER_CONSTANT, value=status_bar_data['status_bar_background'])
        overlay_data['ver_offset'] += int(offset / 2)
    else:
        offset = 0

    # Map external border creation
    img_src = cv2.copyMakeBorder(img_src, overlay_data['border_thickness'], 0, overlay_data['border_thickness'], 0, cv2.BORDER_CONSTANT, value=status_bar_data['overlay_left_top_border'])
    img_src = cv2.copyMakeBorder(img_src, 0, overlay_data['border_thickness'], 0, overlay_data['border_thickness'], cv2.BORDER_CONSTANT, value=status_bar_data['overlay_right_bottom_border'])

    overlay_width = img_src.shape[1]
    overlay_height = img_src.shape[0]

    # Map position
    corners = []
    if overlay_data['overlay_position'] == 0:  # Top left
        start_point = [0, 0]
        end_point = [overlay_width, overlay_height]
        corners.extend([(end_point[0], 0), (img_dst.shape[1] - 1, 0), (img_dst.shape[1] - 1, overlay_data['status_bar_min_height']), (end_point[0], overlay_data['status_bar_min_height'])])
    elif overlay_data['overlay_position'] == 1:  # Top right
        start_point = [img_dst.shape[1] - overlay_width, 0]
        end_point = [img_dst.shape[1], overlay_height]
        corners.extend([(0, 0), (start_point[0] - 1, 0), (start_point[0] - 1, overlay_data['status_bar_min_height']), (0, overlay_data['status_bar_min_height'])])
    elif overlay_data['overlay_position'] == 2:  # Bottom right
        start_point = [img_dst.shape[1] - overlay_width, img_dst.shape[0] - overlay_height]
        end_point = [img_dst.shape[1], img_dst.shape[0]]
        corners.extend([(0, start_point[1] - overlay_data['status_bar_min_height'] + overlay_height - 1), (start_point[0] - 1, start_point[1] - overlay_data['status_bar_min_height'] + overlay_height - 1), (start_point[0] - 1, img_dst.shape[0] - 1), (0, img_dst.shape[0] - 1)])
    elif overlay_data['overlay_position'] == 3:  # Bottom left
        start_point = (0, img_dst.shape[0] - overlay_height)
        end_point = (overlay_width, img_dst.shape[0])
        corners.extend([(end_point[0], start_point[1] - overlay_data['status_bar_min_height'] + overlay_height - 1), (img_dst.shape[1] - 1, start_point[1] - overlay_data['status_bar_min_height'] + overlay_height - 1), (img_dst.shape[1] - 1, img_dst.shape[0] - 1), (end_point[0], img_dst.shape[0] - 1)])

    # Map ratios (needed for correct further transformations)
    width_ratio = src_width / img_src.shape[1]
    height_ratio = src_height / img_src.shape[0]

    overlay_additional_data = {'img_src': img_src,
                               'overlay_dim': [overlay_width, overlay_height],
                               'start_end_points': [start_point, end_point],
                               'corners': corners,
                               'h': h,
                               'width_height_ratio': [width_ratio, height_ratio],
                               'map_offset': offset,
                               'warp_offset': warp_offset,
                               'map_dim': map_dim
                               }

    overlay_data.update(overlay_additional_data)  # Update overlay_data dictionary with the map and its data

    return


def apply_overlay(img_dst, overlay_data, people, status_bar_data, alt):

    # Parameters
    overlay_width = overlay_data['overlay_dim'][0] + overlay_data['border_thickness'] * 2
    overlay_height = overlay_data['overlay_dim'][1] + overlay_data['border_thickness'] * 2
    start_point = overlay_data['start_end_points'][0]
    end_point = overlay_data['start_end_points'][1]

    # Map overlay application
    i = start_point[0]
    io = 0

    while i < end_point[0] and io <= overlay_width:
        j = start_point[1]
        jo = 0
        while j < end_point[1] and jo <= overlay_height:
            img_dst[j][i] = overlay_data['img_src'][jo][io]
            j += 1
            jo += 1
        i += 1
        io += 1

    # Status bar background
    img_dst = cv2.rectangle(img_dst, overlay_data['corners'][0], overlay_data['corners'][2], status_bar_data['status_bar_background'], -1)  # Rectangle
    img_dst = cv2.line(img_dst, overlay_data['corners'][0], overlay_data['corners'][3], status_bar_data['overlay_left_top_border'])  # Left border
    img_dst = cv2.line(img_dst, overlay_data['corners'][0], overlay_data['corners'][1], status_bar_data['overlay_left_top_border'])  # Top border
    img_dst = cv2.line(img_dst, overlay_data['corners'][1], overlay_data['corners'][2], status_bar_data['overlay_right_bottom_border'])  # Right border
    img_dst = cv2.line(img_dst, overlay_data['corners'][3], overlay_data['corners'][2], status_bar_data['overlay_right_bottom_border'])  # Bottom border

    # Adjust people position (if outside map)
    if people[0] is not None:
        add_x = start_point[0] + overlay_data['border_thickness'] + overlay_data['hor_offset']
        add_y = start_point[1] + overlay_data['border_thickness'] + overlay_data['ver_offset']
        dim_x = [start_point[0] + overlay_data['border_thickness'] + overlay_data['hor_offset'], end_point[0] - overlay_data['border_thickness'] + overlay_data['hor_offset']]
        dim_y = [start_point[1] + overlay_data['border_thickness'] + overlay_data['ver_offset'] + overlay_data['map_offset'], end_point[1] - overlay_data['border_thickness'] + overlay_data['ver_offset'] - overlay_data['map_offset'] * 2]

        people[0] = adjust_position(people[0], (add_x, add_y), dim_x, dim_y, overlay_data['position_tolerance'])

    # Draw multiple people
    if people[0] is not None and len(people[0]) > 1:
        # People positions (multi color version)
        v = people[1]  # People that do not respect minimum distance
        for k in range(0, len(people[0])):
            img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 255, 0, 255), -1)
            for l in range(0, len(v)):
                if l == k:
                    img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 0, 255, 255), -1)
        n_people = str(len(people[0]))

    # Draw one person
    elif people[0] is not None and len(people[0]) == 1:
        # People positions (single color version)
        for k in range(0, len(people[0])):
            img_dst = cv2.circle(img_dst, (people[0][k][0], people[0][k][1]), 1, (0, 255, 0, 255), -1)
        n_people = str(1)
    else:
        n_people = str(0)

    # Status bar text
    if alt:  # Safety distance violation
        img_dst = cv2.putText(img_dst, status_bar_data['status_1_alt'] + ' ' + n_people, (overlay_data['corners'][0][0] + status_bar_data['status_1_offset_alt'] - 1, overlay_data['corners'][0][1] + status_bar_data['line_spacing_1_alt']), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_bar_data['status_1_color_alt'], 1)  # First line
        img_dst = cv2.putText(img_dst, status_bar_data['status_2_alt'], (overlay_data['corners'][0][0] + status_bar_data['status_2_offset_alt'] - 1, overlay_data['corners'][0][1] + status_bar_data['line_spacing_2_alt']), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_bar_data['status_2_color_alt'], 1)  # Second line
        img_dst = cv2.putText(img_dst, status_bar_data['status_3_alt'], (overlay_data['corners'][0][0] + status_bar_data['status_3_offset_alt'] - 1, overlay_data['corners'][0][1] + status_bar_data['line_spacing_3_alt']), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_bar_data['status_3_color_alt'], 1)  # Third line
    else:  # No safety distance violation
        img_dst = cv2.putText(img_dst, status_bar_data['status_1'] + ' ' + n_people, (overlay_data['corners'][0][0] + status_bar_data['status_1_offset'] - 1, overlay_data['corners'][0][1] + status_bar_data['line_spacing_1']), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_bar_data['status_1_color'], 1)  # First line
        img_dst = cv2.putText(img_dst, status_bar_data['status_2'], (overlay_data['corners'][0][0] + status_bar_data['status_2_offset'] - 1, overlay_data['corners'][0][1] + status_bar_data['line_spacing_2']), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_bar_data['status_2_color'], 1)  # Second line
        img_dst = cv2.putText(img_dst, status_bar_data['status_3'], (overlay_data['corners'][0][0] + status_bar_data['status_3_offset'] - 1, overlay_data['corners'][0][1] + status_bar_data['line_spacing_3']), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_bar_data['status_3_color'], 1)  # Third line

    return img_dst
