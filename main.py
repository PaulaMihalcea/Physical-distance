import cv2
import numpy as np
import sys
from configparser import ConfigParser
from process_frame import process_frame_first, process_frame


def main(src, save=None, dst_name=None):

    print('')
    print('Welcome to the Physical Distance Detector!')
    print('')

    # Setup
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    pts_src_ini = f.get('General', 'pts_src')  # Source points (for warp)
    if pts_src_ini == 'None':
        pts_src = None
    else:
        pts_src = []
        pts_src_ini = pts_src_ini.split('\n')
        for i in range(0, len(pts_src_ini)):
            pts_src.append([int(pts_src_ini[i].split(' ')[0]), int(pts_src_ini[i].split(' ')[1])])
        pts_src = np.array(pts_src)
        print('Reference points have been found.')

    pts_dst_ini = f.get('General', 'pts_dst')  # Destination points (can be either automatically calculated or manually specified)
    if pts_dst_ini == 'None':
        pts_dst = None
    else:
        pts_dst = []
        pts_dst_ini = pts_dst_ini.split('\n')
        for i in range(0, len(pts_dst_ini)):
            pts_dst.append([int(pts_dst_ini[i].split(' ')[0]), int(pts_dst_ini[i].split(' ')[1])])
        pts_dst = np.array(pts_dst)
        print('Destination points have been found.')

    print('')

    map_dim = [f.getfloat('General', 'map_width') * 100, f.getfloat('General', 'map_height') * 100]  # Real map dimensions
    min_distance = f.getfloat('General', 'min_distance') * 100

    if save is None:
        save = f.get('System', 'default_save')  # Get the default save setting if it has not been specified in the command line arguments
    max_attempts = f.getint('System', 'max_attempts')  # Maximum video reading attempts before quitting

    status = [[f.get('Status bar text', 'status_1'), tuple(map(int, f.get('Status bar colors', 'status_1_color').split(', '))), f.getint('Status bar text', 'status_1_offset'), f.getint('Status bar text', 'line_spacing_1')],
              [f.get('Status bar text', 'status_2'), tuple(map(int, f.get('Status bar colors', 'status_2_color').split(', '))), f.getint('Status bar text', 'status_2_offset'), f.getint('Status bar text', 'line_spacing_2')],
              [f.get('Status bar text', 'status_3'), tuple(map(int, f.get('Status bar colors', 'status_3_color').split(', '))), f.getint('Status bar text', 'status_3_offset'), f.getint('Status bar text', 'line_spacing_3')]
              ]  # Overlay status text

    status_alt = [[f.get('Status bar text', 'status_1_alt'), tuple(map(int, f.get('Status bar colors', 'status_1_alt_color').split(', '))), f.getint('Status bar text', 'status_1_alt_offset'), f.getint('Status bar text', 'line_spacing_1_alt')],
                  [f.get('Status bar text', 'status_2_alt'), tuple(map(int, f.get('Status bar colors', 'status_2_alt_color').split(', '))), f.getint('Status bar text', 'status_2_alt_offset'), f.getint('Status bar text', 'line_spacing_2_alt')],
                  [f.get('Status bar text', 'status_3_alt'), tuple(map(int, f.get('Status bar colors', 'status_3_alt_color').split(', '))), f.getint('Status bar text', 'status_3_alt_offset'), f.getint('Status bar text', 'line_spacing_3_alt')]
                  ]  # Overlay alternative status text

    # Video stream loading
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
    process, overlay_data, map_ratio = process_frame_first(cap, src, pts_src, pts_dst, map_dim, min_distance, [status, status_alt], out)

    if not process:  # Exit program if process_first_frame() returns False
        print('An error occurred or the user closed the window. Exiting program...')
        sys.exit()

    # Video processing
    while process:
        process = process_frame(cap, src, overlay_data, map_ratio, min_distance, [status, status_alt], out)

    # Final operations
    cap.release()  # Release capture when finished

    if save:
        out.release()
        print('Video saved as ' + output_video + '.')
        print('')

    cv2.destroyAllWindows()  # Close window

    print('Exiting program...')
    sys.exit(0)  # Exit program


# TODO prova la versione da linea di comando:
'''
if __name__ == '__main__':
    src = sys.argv[0]
    save = sys.argv[1]
    dst_name = sys.argv[2]

    main(src, save, dst_name)
'''





# TODO Delete tests below:

src = 'test/test_s.mp4'
# src = 'openpose/examples/media/video.avi'
save = True

main(src, save)


# Parametri da riga di comando:
# source (file da leggere oppure webcam) (opzionale, se vuoto prende la webcam)
# save (se salvare il risultato o no) (opzionale, default no)
# destination file name (opzionale)
