import cv2
import numpy as np
from utils import get_click_src, get_man_src
from overlay import generate_overlay, apply_overlay
from transform_coord import transform_coord


def process_frame_first(cap, src, pts_src, pts_dst, map_dim, min_distance, people, status, out):

    _, frame = cap.read()  # Frame by frame capture; returns a boolean (True if the frame has been read correctly, False otherwise) and a frame

    if frame is not None:

        if pts_src is None:
            while True:
                ans = input('Would you like to click on the video in order to create an overlay (C),\n'
                            'or do you prefer to insert source pixels manually (M)? ')
                print('')

                if ans is 'c' or ans is 'C':
                    pts_src = get_click_src(frame)
                    break
                elif ans is 'm' or ans is 'M':
                    pts_src = get_man_src()
                    break
                else:
                    print('Invalid answer.')

        overlay_data = generate_overlay(frame, pts_src, pts_dst)  # Generate overlay

        map_ratio = [map_dim[0] / overlay_data['overlay_dim'][0], map_dim[1] / overlay_data['overlay_dim'][1]]

        people, v = transform_coord(people, overlay_data['h'], overlay_data['width_height_ratio'], map_ratio, min_distance)

        # Frame overlay
        if len(v) > 0:
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


def process_frame(cap, src, overlay_data, map_ratio, min_distance, people, status, out):
    _, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        people, v = transform_coord(people, overlay_data['h'], overlay_data['width_height_ratio'], map_ratio, min_distance)

        # Frame overlay
        if len(v) > 0:
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
