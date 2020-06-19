import numpy as np
import cv2

def read_file(input_video, save=False, fps=20.0):

    cap = cv2.VideoCapture(input_video)  # 0 or -1 For default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file

    if save:
        output_video = input_video + '_output.avi'  # TODO Aggiungi estensione automatica in base al file di input
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # Defines the codec and creates a VideoWriter object
        out = cv2.VideoWriter(output_video, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    frame_number = 0  # Frame counter
    position = (5, int(cap.get(4) - 10))  # Text position

    if not cap.isOpened():  # Check that the capture has been initialized
        cap.open()

    while True:

        ret, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame

        if frame is not None:
            frame_number += 1
            f = str(frame_number)

            # Frame processing
            cv2.putText(frame, f, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0, 255), 3)

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


input_video = 'test/test_s.mp4'

read_file(input_video, save=True)
