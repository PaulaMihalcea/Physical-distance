import os
import cv2
import sys
from get_points import get_points
from overlay import generate_overlay, apply_overlay
from transform_coords import transform_coords


# OpenPose initialization

# Requires OpenCV installed for Python
# Import for Ubuntu/OSX

try:
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Current project's main folder path

    try:
        sys.path.append(dir_path + '/openpose/build/python/openpose')  # OpenPose Python library path
        import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found.')
        raise e

    # Parameters
    params = dict()
    params['model_folder'] = dir_path + '/openpose/models'  # Models folder
    params['logging_level'] = 255  # No logging

    # Start OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

except Exception as e:
    print(e)
    sys.exit(-1)


def process_frame_first(cap, src, out, mode, floor_data, mat_data, overlay_data, status_bar_data, min_distance):

    _, frame = cap.read()  # Frame by frame capture; returns a boolean (True if the frame has been read correctly, False otherwise) and a frame

    if frame is not None:

        get_points(frame, floor_data, mat_data, mode)  # Get source points

        generate_overlay(frame, floor_data, mat_data, status_bar_data, overlay_data, mode)  # Generate overlay

        if mode:  # Real map dimensions for floor mode
            map_dim = [floor_data['floor_width'], floor_data['floor_width']]
            floor_ratio = [map_dim[0] / overlay_data['overlay_dim'][0], map_dim[1] / overlay_data['overlay_dim'][1]]
        elif not mode:  # Real map dimensions for mat mode
            map_dim = overlay_data['map_dim']
            floor_ratio = [map_dim[0] / overlay_data['overlay_dim'][0], map_dim[1] / overlay_data['overlay_dim'][1]]

        # OpenPose image processing
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        frame = datum.cvOutputData

        # People's position estimation
        people, v, points_p = transform_coords(datum.poseKeypoints, overlay_data['h'], overlay_data['width_height_ratio'], floor_ratio, min_distance, overlay_data['warp_offset'])

        # Frame overlay
        if v is not None and len(v) > 0:
            frame = apply_overlay(frame, overlay_data, [people, v], status_bar_data, True)
        else:
            frame = apply_overlay(frame, overlay_data, [people, v], status_bar_data, False)

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
            return False, None

    else:
        return False, None

    return True, floor_ratio, points_p


def process_frame(cap, src, out, overlay_data, status_bar_data, min_distance, floor_ratio, position_alpha, points_p):

    _, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        # OpenPose image processing
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        frame = datum.cvOutputData

        # People's position estimation
        people, v, points_p = transform_coords(datum.poseKeypoints, overlay_data['h'], overlay_data['width_height_ratio'], floor_ratio, min_distance, overlay_data['warp_offset'], position_alpha, points_p)

        # Frame overlay
        if v is not None and len(v) > 0:
            frame = apply_overlay(frame, overlay_data, [people, v], status_bar_data, True)
        else:
            frame = apply_overlay(frame, overlay_data, [people, v], status_bar_data, False)

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
            return False, None

    else:
        return False, None

    return True, points_p
