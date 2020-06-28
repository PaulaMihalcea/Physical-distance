import cv2
import numpy as np
import sys
from configparser import ConfigParser

from get_people_position import get_people_position
from process_frame import process_frame_first, process_frame


def main(src, save=None, dst_name=None):

    # Setup
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    floor_corners = f.get('General', 'floor_corners')  # Floor corners setup
    if floor_corners == 'None':
        pts_src = None
    else:
        pts_src = []
        floor_corners = floor_corners.split('\n')
        for i in range(0, len(floor_corners)):
            pts_src.append([int(floor_corners[i].split(' ')[0]), int(floor_corners[i].split(' ')[1])])
        pts_src = np.array(pts_src)

    if save is None:
        save = f.get('System', 'default_save')  # Get the default save setting if it has not been specified in the command line arguments
    max_attempts = f.getint('System', 'max_attempts')  # Maximum video reading attempts before quitting

    status = [(f.get('Status bar text', 'status_1'), f.get('Status bar text', 'status_1_color')), (f.get('Status bar text', 'status_2'), f.get('Status bar text', 'status_2_color')), (f.get('Status bar text', 'status_3'), f.get('Status bar text', 'status_3_color'))]  # Overlay status text

    status_alt = [(f.get('Status bar text', 'status_1_alt'), f.get('Status bar text', 'status_1_alt_color')), (f.get('Status bar text', 'status_2_alt'), f.get('Status bar text', 'status_2_alt_color')), (f.get('Status bar text', 'status_3_alt'), f.get('Status bar text', 'status_3_alt_color'))]  # Overlay alternative status text

    # Video stream loading
    print('Welcome to the Physical Distance Detector!')
    print('')

    cap = cv2.VideoCapture(src)  # 0 or -1 for default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file
    attempt = 0

    while not cap.isOpened() and attempt < max_attempts:  # Check that the capture has been initialized
        cap.open()
        attempt += 1

    if not cap.isOpened() and attempt == max_attempts:  # Exit if the capture has not been initialized after a number of attempts
        print('Could not open video stream. Exiting program...')
        sys.exit(-1)  # Exit program

    # Output video parameters
    if save:
        if dst_name is not None:
            output_video = dst_name.replace('.' + dst_name.partition('.')[len(dst_name.partition('.')) - 1], '.avi')  # Sets the specified name for the output video (replacing the original extension)...
        else:
            output_video = src[::-1].partition('.')[2].partition('/')[0][::-1] + '_output.avi'  # ...or just gets the input name and adds '_output.avi' at the end

        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Defines the codec and creates a VideoWriter object
        fps = f.getfloat('General', 'fps')  # Number of frames per second of the output video

        out = cv2.VideoWriter(output_video, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
    else:
        out = None  # If the video is not to be saved, a null argument is passed

    # First frame processing
    people = get_people_position()
    process, overlay_data = process_frame_first(cap, src, pts_src, people, status, out)

    if not process:  # Exit program if process_first_frame() returns False
        print('An error occurred or the user closed the window. Exiting program...')
        sys.exit()

    # Video processing
    while process:
        people = get_people_position()
        process = process_frame(cap, src, overlay_data, people, status, out)

    # Final operations
    cap.release()  # Release capture when finished

    if save:
        out.release()
        print('Video saved as ' + output_video + '.')
        print('')

    cv2.destroyAllWindows()  # Close window

    print('Exiting program...')
    sys.exit(0)  # Exit program


'''
if __name__ == "__main__":
    src = sys.argv[0]
    save = sys.argv[1]
    dst_name = sys.argv[2]

    main(src, save, dst_name)
'''





# TODO Delete tests below:

src = 'test/test_s.mp4'
save = False

main(src, save)


# Parametri da riga di comando:
# source (file da leggere oppure webcam) (opzionale, se vuoto prende la webcam)
# save (se salvare il risultato o no) (opzionale, default no)
# destination file name (opzionale)
