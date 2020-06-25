import sys
import cv2
import numpy as np
from overlay import generate_overlay, apply_overlay


def process_first_frame(cap, overlay_position, overlay_height, points, status_1, status_2, status_3, out=None):

    bool, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:
        frame_counter = 1  # Frame counter (debug only)  # TODO

        overlay_data = {'img_src': None,
                        'overlay_position': None,
                        'overlay_dim': None,
                        'start_point': None,
                        'end_point': None,
                        'corners': None}

        overlay_data = generate_overlay(frame, overlay_position, overlay_height)  # Generate actual overlay

        # Frame overlay
        frame = apply_overlay(frame, overlay_data[0], overlay_data[1], overlay_data[2], overlay_data[3], overlay_data[4], overlay_data[5], points, status_1, status_2, status_3)
        # frame = cv2.putText(frame, str(frame_counter), (5, int(cap.get(4)) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)  # Frame counter overlay (debug only)

        # Save
        if save:
            out.write(frame)

        # Window name
        if isinstance(src, int):
            window_name = 'Webcam'
        else:
            window_name = src

        # Display result
        cv2.imshow(window_name, frame)
        k = cv2.waitKey(33)
        if k == 27:
            return False

    else:
        return False

    return True, overlay_data


def process_frame(cap, overlay_data, frame_counter, points, status_1, status_2, status_3, out=None):  # TODO check parameters
    bool, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        # Frame overlay
        frame = apply_overlay(frame, overlay_data[0], overlay_data[1], overlay_data[2], overlay_data[3], overlay_data[4], overlay_data[5], points, status_1, status_2, status_3)
        # frame = cv2.putText(frame, str(frame_counter), (5, int(cap.get(4)) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)  # Frame counter overlay (debug only)

        # Save
        if save:
            out.write(frame)

        # Window name
        if isinstance(src, int):
            window_name = 'Webcam'
        else:
            window_name = src

        # Display result
        cv2.imshow(window_name, frame)
        k = cv2.waitKey(33)
        if k == 27:
            return False

    else:
        return False

    return True









def main(src, save=False, dst_name=None, fps=30.0, overlay_pos=0):

    status_1 = ('People detected: 20', (255, 255, 0, 255))
    status_2 = ('SAFETY DISTANCE', (0, 0, 255, 255))
    status_3 = ('VIOLATION!', (0, 0, 255, 255))
    status_2 = ('SAFETY DISTANCE', (0, 255, 0, 255))
    status_3 = ('RESPECTED', (0, 255, 0, 255))

    people = np.array([[85, 366], [180, 385], [87, 367], [146, 421]])  # Posizioni in test_s_1, test_s_2, test_s_3 (media calcolata a mano), più punti di prova

    print('Welcome to the Physical Distance Detector!')
    print('')

    # Load video stream
    cap = cv2.VideoCapture(src)  # 0 or -1 For default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file
    attempt = 0
    while not cap.isOpened() and attempt < 5:  # Check that the capture has been initialized
        cap.open()
        attempt += 1
    if not cap.isOpened() and attempt == 5:
        print('Error opening video stream. Exiting program...')
        sys.exit(-1)

    # Video stream info
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Status bar parameters
    minimap_height = 80
    text_pos = (5, height - 10)  # Text position

    # Output video parameters
    if save:
        if dst_name is not None:
            output_video = dst_name.replace('.' + dst_name.partition('.')[len(dst_name.partition('.')) - 1], '.avi')
        else:
            output_video = src[::-1].partition('.')[2].partition('/')[0][::-1] + '_output.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # Defines the codec and creates a VideoWriter object
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))







    # First frame processing
    frame_counter = 1

    overlay_position = overlay_pos
    overlay_height = 80

    if save:
        process, overlay_data = process_first_frame(cap, overlay_position, overlay_height, people, status_1, status_2, status_3, out)
    else:
        process, overlay_data = process_first_frame(cap, overlay_position, overlay_height, people, status_1, status_2, status_3)






    # Video processing
    while process:
        frame_counter += 1  # Frame counter (debug only)  # TODO
        if save:
            process = process_frame(cap, overlay_data, frame_counter, people, status_1, status_2, status_3, out)
        else:
            process = process_frame(cap, overlay_data, frame_counter, people, status_1, status_2, status_3)

    # FINAL RELEASES
    cap.release()  # Release capture when finished
    if save:
        out.release()
        print('Video saved as ' + output_video + '.')
        print('')
    cv2.destroyAllWindows()  # Close window

    print('Exiting program...')
    sys.exit()  # Exit the whole program



# TODO Delete tests below:

src = 'test/test_s.mp4'
save = True
overlay_pos = 0

main(src, save, overlay_pos=overlay_pos)
