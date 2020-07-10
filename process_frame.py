import os
import cv2
import sys
import inspect
import numpy as np
from utils import get_points_mouse, get_points_chessboard
from overlay import generate_overlay, apply_overlay
from transform_coords import transform_coords
from get_dim import get_dim


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


def process_frame_first(cap, src, mode, map_data, chessboard_data, min_distance, status_bar, overlay_data, out):

    _, frame = cap.read()  # Frame by frame capture; returns a boolean (True if the frame has been read correctly, False otherwise) and a frame

    if frame is not None:

        status_bar_text = status_bar[1]

        if mode:  # Map
            if map_data['map_src'] is None:
                map_data['map_src'], map_data['map_dst'], dst_dim = get_points_mouse(frame, map_data, mode)
            elif map_data['map_src'] is not None:
                # Get destination points
                if map_data['map_dst'] is None:
                    dst_width, dst_height = get_dim(map_data['map_src'], mode, map_data['ratio'])  # Calculate dimensions of destination image
                    map_data['map_dst'] = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]])  # Set destination points
                else:
                    dst_width, dst_height = get_dim(map_data['map_dst'], mode, map_data['ratio'])  # Calculate dimensions of destination image
                    dst_width += 1  # TODO perché +=1?
                    dst_height += 1
                dst_dim = (dst_width, dst_height)

        elif not mode:  # Chessboard
            if chessboard_data['chessboard_src'] is None:
                chessboard_data['chessboard_src'], chessboard_data['pts_dst'], dst_dim = get_points_chessboard(frame, chessboard_data['chessboard_src'], mode)
            else:
                _, chessboard_data['pts_dst'], dst_dim = get_points_chessboard(frame, chessboard_data['chessboard_src'], mode)

        else:  # Shouldn't even get to this point, but whatever
            print('An error occurred in the ' + inspect.stack()[0][3] + ' function, exiting program.')
            sys.exit(-1)

        overlay_new_data = generate_overlay(frame, map_data, chessboard_data, status_bar[0], overlay_data, mode, dst_dim)  # Generate overlay  # TODO dst_dim potrebbe causare problemi in alcuni casi

        if mode:
            map_dim = [map_data['map_width'], map_data['map_width']]  # Real map dimensions
            map_ratio = [map_dim[0] / overlay_new_data['overlay_dim'][0], map_dim[1] / overlay_new_data['overlay_dim'][1]]
        elif not mode:
            map_dim = overlay_new_data['map_dim']
            map_ratio = [map_dim[0] / overlay_new_data['overlay_dim'][0], map_dim[1] / overlay_new_data['overlay_dim'][1]]

        # OpenPose image processing
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        frame = datum.cvOutputData

        people, v = transform_coords(datum.poseKeypoints, overlay_new_data['h'], overlay_new_data['width_height_ratio'], map_ratio, min_distance, overlay_new_data['warp_offset'])

        # Frame overlay
        if v is not None and len(v) > 0:
            frame = apply_overlay(frame, overlay_new_data, [people, v], status_bar_text[1])
        else:
            frame = apply_overlay(frame, overlay_new_data, [people, v], status_bar_text[0])

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

    return True, overlay_new_data, map_ratio


def process_frame(cap, src, overlay_data, map_ratio, min_distance, status_bar, out):
    _, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        status_bar_text = status_bar[1]

        # OpenPose image processing
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        frame = datum.cvOutputData

        people, v = transform_coords(datum.poseKeypoints, overlay_data['h'], overlay_data['width_height_ratio'], map_ratio, min_distance, overlay_data['warp_offset'])

        # Frame overlay
        if v is not None and len(v) > 0:
            frame = apply_overlay(frame, overlay_data, [people, v], status_bar_text[1])
        else:
            frame = apply_overlay(frame, overlay_data, [people, v], status_bar_text[0])

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
