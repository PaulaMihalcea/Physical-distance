import sys
import cv2
from overlay import overlay
from warp import warp


def process_frame(cap, overlay_src, frame_counter, height, out=None):
    bool, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

    if frame is not None:

        # Frame overlay
        frame = overlay(frame, overlay_src, position=overlay_pos)
        frame = cv2.putText(frame, str(frame_counter), (5, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)  # Frame counter overlay (debug only)

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
    frame_counter = 2  # Frame counter (debug only)  # TODO
    bool, frame = cap.read()
    overlay_src = warp(frame, 1)

    if save:
        process = process_frame(cap, overlay_src, frame_counter, height, out)
    else:
        process = process_frame(cap, overlay_src, frame_counter, height)








    # Video processing
    while process:
        frame_counter += 1  # Frame counter (debug only)  # TODO
        if save:
            process = process_frame(cap, overlay_src, frame_counter, height, out)
        else:
            process = process_frame(cap, overlay_src, frame_counter, height)

    # Final releases
    cap.release()  # Release capture when finished
    if save:
        out.release()
    cv2.destroyAllWindows()  # Close window

    return



# TODO Delete tests below:

src = 'test/test_s.mp4'
save = True
overlay_pos = 2

main(src, save, overlay_pos=overlay_pos)
