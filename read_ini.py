import numpy as np
from configparser import ConfigParser


def process_color(color_ini):

    color = tuple(map(int, color_ini.split(',')))

    return color


def process_points(points_ini):

    if points_ini == 'None':
        points = None
    else:
        points = []
        points_ini = points_ini.split('\n')
        for i in range(0, len(points_ini)):
            points.append([int(points_ini[i].split(' ')[0]), int(points_ini[i].split(' ')[1])])
        points = np.array(points)

    return points


def read_ini(ini_file):

    f = ConfigParser()
    f.read(ini_file)  # Parse the setup.ini file to retrieve settings

    system_data = {
        'min_distance': f.getfloat('System', 'min_distance') * 100,  # Safety distance that people should keep between them, converted from meters (in the setupfile) to centimeters
        'default_save': f.getboolean('System', 'default_save'),  # Get the default save setting if it has not been specified in the command line arguments
        'fps': f.getfloat('System', 'fps'),  # Number of frames per second of the output video
        'max_attempts': f.getint('System', 'max_attempts'),  # Maximum video reading attempts before quitting
        'position_alpha': f.getfloat('System', 'position_alpha')
    }

    map_data = {
        'map_width': f.getfloat('Map', 'map_width') * 100,  # Real floor width in centimeters; it must be given in meters in the setup file
        'map_height': f.getfloat('Map', 'map_height') * 100,  # Real floor height in centimeters; it must be given in meters in the setup file
        'ratio': f.getfloat('Map', 'ratio'),  # Floor width/height ratio; useful in some cases to correct perspective
        'map_src': process_points(f.get('Map', 'map_src')),  # Floor source points
        'map_dst': process_points(f.get('Map', 'map_dst'))  # Floor destination points
    }

    mat_data = {
        'mat_width': f.getfloat('Mat', 'mat_width') * 100,
        'mat_height': f.getfloat('Mat', 'mat_height') * 100,
        'roi_x': f.getfloat('Mat', 'roi_x') * 100,
        'roi_y': f.getfloat('Mat', 'roi_y') * 100,
        'mat_src': process_points(f.get('Mat', 'mat_src')),
        'mat_dst': None
    }

    overlay_data = {
        'overlay_position': f.getint('Overlay', 'overlay_position'),  # Overlay position on the video (0: top left; 1: top right; 2: bottom right; 3: bottom left)
        'border_thickness': f.getint('Overlay', 'border_thickness'),  # Overlay border thickness in pixels
        'overlay_max_height': f.getint('Overlay', 'overlay_max_height'),
        'status_bar_min_width': f.getint('Overlay', 'status_bar_min_width'),  # Minimum status bar width
        'status_bar_min_height': f.getint('Overlay', 'status_bar_min_height'),  # Minimum status bar height
        'hor_offset': f.getint('Overlay', 'hor_offset'),  # Manual horizontal offset (for people representation)
        'ver_offset': f.getint('Overlay', 'ver_offset'),  # Manual vertical offset (for people representation)
        'position_tolerance': f.getint('Overlay', 'position_tolerance'),
    }

    status_bar_data = {
        'status_1': f.get('Status bar', 'status_1'),  # Overlay status text
        'status_2': f.get('Status bar', 'status_2'),
        'status_3': f.get('Status bar', 'status_3'),
        'status_1_color': process_color(f.get('Status bar', 'status_1_color')),
        'status_2_color': process_color(f.get('Status bar', 'status_2_color')),
        'status_3_color': process_color(f.get('Status bar', 'status_3_color')),
        'line_spacing_1': f.getint('Status bar', 'line_spacing_1'),
        'line_spacing_2': f.getint('Status bar', 'line_spacing_2'),
        'line_spacing_3': f.getint('Status bar', 'line_spacing_3'),
        'status_1_offset': f.getint('Status bar', 'status_1_offset'),
        'status_2_offset': f.getint('Status bar', 'status_2_offset'),
        'status_3_offset': f.getint('Status bar', 'status_3_offset'),

        'status_1_alt': f.get('Status bar', 'status_1_alt'),  # Overlay alternative status text
        'status_2_alt': f.get('Status bar', 'status_2_alt'),
        'status_3_alt': f.get('Status bar', 'status_3_alt'),
        'status_1_color_alt': process_color(f.get('Status bar', 'status_1_color_alt')),
        'status_2_color_alt': process_color(f.get('Status bar', 'status_2_color_alt')),
        'status_3_color_alt': process_color(f.get('Status bar', 'status_3_color_alt')),
        'line_spacing_1_alt': f.getint('Status bar', 'line_spacing_1_alt'),
        'line_spacing_2_alt': f.getint('Status bar', 'line_spacing_2_alt'),
        'line_spacing_3_alt': f.getint('Status bar', 'line_spacing_3_alt'),
        'status_1_offset_alt': f.getint('Status bar', 'status_1_offset_alt'),
        'status_2_offset_alt': f.getint('Status bar', 'status_2_offset_alt'),
        'status_3_offset_alt': f.getint('Status bar', 'status_3_offset_alt'),

        'status_bar_background': process_color(f.get('Status bar', 'status_bar_background')),
        'overlay_left_top_border': process_color(f.get('Status bar', 'overlay_left_top_border')),
        'overlay_right_bottom_border': process_color(f.get('Status bar', 'overlay_right_bottom_border')),
    }

    return system_data, map_data, mat_data, overlay_data, status_bar_data
