import cv2

from overlay import generate_overlay, apply_overlay
from transform_coord import transform_coord


def process_frame_first(cap, src, overlay_position, people, status, out):

    _, frame = cap.read()  # Frame by frame capture; returns a boolean (True if the frame has been read correctly, False otherwise) and a frame

    if frame is not None:

        overlay_data = generate_overlay(frame, overlay_position)  # Generate overlay

        people = transform_coord(people, overlay_data[6], overlay_data[7])

        # Frame overlay
        frame = apply_overlay(frame, overlay_data[0], overlay_data[1], overlay_data[2], overlay_data[3], overlay_data[4], overlay_data[5], people, status)
        # frame = cv2.putText(frame, str(frame_counter), (5, int(cap.get(4)) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)  # Frame counter overlay (debug only)

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

    return True, overlay_data


def process_frame(cap, src, overlay_data, people, status, out):  # TODO check parameters
    bool, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        people = transform_coord(people, overlay_data[6], overlay_data[7])

        # Frame overlay
        frame = apply_overlay(frame, overlay_data[0], overlay_data[1], overlay_data[2], overlay_data[3], overlay_data[4], overlay_data[5], people, status)

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
