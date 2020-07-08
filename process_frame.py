import os
import cv2
import sys
import numpy as np
from configparser import ConfigParser
from utils import get_points_mouse, get_points_chessboard
from overlay import generate_overlay, generate_overlay_c, apply_overlay
from transform_coords import transform_coords, transform_coords_c
from get_dst_dim import get_dst_dim


# OpenPose initialization

# Requires OpenCV installed for Python
# Import for Ubuntu/OSX

try:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        sys.path.append(dir_path + '/openpose/build/python/openpose')
        import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found.')
        raise e

    # Parameters
    params = dict()
    params['model_folder'] = dir_path + '/openpose/models'
    params['logging_level'] = 255

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

except Exception as e:
    print(e)
    sys.exit(-1)


def process_frame_first(cap, src, chessboard, pts_src, pts_src_chessboard, pts_dst, map_dim, min_distance, status, out):

    _, frame = cap.read()  # Frame by frame capture; returns a boolean (True if the frame has been read correctly, False otherwise) and a frame

    if frame is not None:

        if not chessboard:

            if pts_src is None:
                pts_src, pts_dst, dst_dim = get_points_mouse(frame, pts_dst)
            elif pts_src is not None:
                f = ConfigParser()
                f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

                ratio = f.getfloat('General', 'ratio')
                # Get destination points
                if pts_dst is None:
                    dst_width, dst_height = get_dst_dim(pts_src, ratio)  # Calculate dimensions of destination image
                    pts_dst = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]])  # Set destination points
                else:
                    dst_width, dst_height = get_dst_dim(pts_dst, ratio)  # Calculate dimensions of destination image
                    dst_width += 1
                    dst_height += 1
                dst_dim = (dst_width, dst_height)

            overlay_data = generate_overlay(frame, pts_src, pts_dst, dst_dim)  # Generate overlay  # TODO dst_dim potrebbe causare problemi in alcuni casi

        else:  # chessboard = True
            if pts_src is None:
                pts_src, pts_dst, pts_dst_chessboard, dst_dim = get_points_chessboard(frame, pts_src, pts_src_chessboard, pts_dst)
            else:
                _, pts_dst, pts_dst_chessboard, dst_dim = get_points_chessboard(frame, pts_src, pts_src_chessboard, pts_dst)

            overlay_data = generate_overlay_c(frame, pts_src_chessboard)  # Generate overlay  # TODO potrebbe causare problemi in alcuni casi

        if not chessboard:
            map_ratio = [map_dim[0] / overlay_data['overlay_dim'][0], map_dim[1] / overlay_data['overlay_dim'][1]]
        else:
            map_dim = overlay_data['map_dim']
            map_ratio = [map_dim[0] / overlay_data['overlay_dim'][0], map_dim[1] / overlay_data['overlay_dim'][1]]

        # OpenPose image processing
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        frame = datum.cvOutputData

        people, v = transform_coords(datum.poseKeypoints, overlay_data['h'], overlay_data['width_height_ratio'], map_ratio, min_distance)

        # Frame overlay
        if v is not None and len(v) > 0:
            frame = apply_overlay(frame, overlay_data, [people, v], status[1])
        else:
            frame = apply_overlay(frame, overlay_data, [people, v], status[0])

        # Save
        if out is not None:
            out.write(frame)

        # Window name
        if isinstance(src, int):
            window_name = 'Webcam'
        else:
            window_name = src[::-1].partition('.')[2].partition('/')[0][::-1]  # Source name (file name only, no path)

        # Display result
        cv2.imshow(window_name, frame)
        k = cv2.waitKey(33)
        if k == 27:
            return False

    else:
        return False

    return True, overlay_data, map_ratio


def process_frame(cap, src, overlay_data, map_ratio, min_distance, status, out):
    _, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        # OpenPose image processing
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        frame = datum.cvOutputData

        people, v = transform_coords_c(datum.poseKeypoints, overlay_data['h'], overlay_data['width_height_ratio'], map_ratio, min_distance, overlay_data['warp_offset'])  # TODO

        # Frame overlay
        if v is not None and len(v) > 0:
            frame = apply_overlay(frame, overlay_data, [people, v], status[1])
        else:
            frame = apply_overlay(frame, overlay_data, [people, v], status[0])

        # Save
        if out is not None:
            out.write(frame)

        # Window name
        if isinstance(src, int):
            window_name = 'Webcam'
        else:
            window_name = src[::-1].partition('.')[2].partition('/')[0][::-1]  # Source name (file name only, no path)

        # Display result
        cv2.imshow(window_name, frame)
        k = cv2.waitKey(33)
        if k == 27:
            return False

    else:
        return False

    return True
