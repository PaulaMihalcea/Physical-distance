import sys
import cv2
from overlay import overlay

def main(input_video, save=False, fps=20.0, position=0):

    cap = cv2.VideoCapture(input_video)  # 0 or -1 For default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file

    width = int(cap.get(3))
    height = int(cap.get(4))

    # Minimap parameters
    minimap_height = 80

    if save:
        output_video = input_video[::-1].partition('.')[2].partition('/')[0][::-1] + '_overlay_output.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # Defines the codec and creates a VideoWriter object
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_number = 0  # Frame counter
    position = (5, height - 10)  # Text position

    if not cap.isOpened():  # Check that the capture has been initialized
        cap.open()

    while True:

        ret, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

        if frame is not None:
            frame_number += 1
            f = str(frame_number)

            # Frame processing
            # cv2.putText(frame, f, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0, 255), 3)  # Frame counter (debug only)
            # cv2.rectangle(frame, start_point, end_point, color, thickness)
            frame = overlay(frame, cv2.imread('test/stone.jpg'))

            if save:
                out.write(frame)

            if isinstance(input_video, int):
                window_name = 'Webcam'
            else:
                window_name = input_video

            cv2.imshow(window_name, frame)
            k = cv2.waitKey(33)
            if k == 27:
                break
        else:
            break

    cap.release()  # Release the capture when finished

    if save:
        out.release()

    cv2.destroyAllWindows()

    return


input_video = 'test/test_s.mp4'

main(input_video, save=True)
