import numpy as np
import cv2

input = 'output.avi'
cap = cv2.VideoCapture(input)  # 0 or -1 For default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file

save_to = 'output2.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Defines the codec and creates a VideoWriter object
out = cv2.VideoWriter(save_to, fourcc, 20.0, (640,480))

frame_number = 0  # Frame counter
position = (5, int(cap.get(4) - 10))  # Text position

while True:

    if not cap.isOpened():  # Check that the capture has been initialized
        cap.open()

    ret, frame = cap.read()  # Frame by frame capture; returns a boolean: True if the frame has been read correctly, False otherwise; also returns a frame
    frame_number += 1
    f = str(frame_number)

    # Frame processing
    cv2.putText(frame, f, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0, 255), 3)

    out.write(frame)

    if isinstance(input, int):
        window_name = 'Webcam'
    else:
        window_name = input
    cv2.imshow(window_name, frame)
    k = cv2.waitKey(33)
    if k == 27:
        break

cap.release()  # Release the capture when finished
out.release()
cv2.destroyAllWindows()
