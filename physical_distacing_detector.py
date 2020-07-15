import cv2
import sys
import inspect
import numpy as np
from read_ini import read_ini
from process_frame import process_frame_first, process_frame


def main(src, save=None, dst_name=None, setup_file='setup.ini'):

    print('')
    print('Welcome to the Physical Distancing Detector!')
    print('')
    print(src, type(src))
    # Parameters
    if src == '0' or src == '-1':
        src = 0
    print(src, type(src))

    if dst_name is not None:
        dst_name_parts = dst_name.split('.')
        if len(dst_name_parts) == 1:
            dst_name += '.avi'
        elif dst_name_parts[len(dst_name_parts) - 1] != 'avi':
            dst_name = ''
            for i in range(0, len(dst_name_parts) - 1):
                dst_name += str(dst_name_parts[i]) + '.'
            dst_name += 'avi'
    system_data, map_data, mat_data, overlay_data, status_bar_data = read_ini(setup_file)
    mode = None  # If True, map reference points of that type have been found; if False, mat reference points have been found

    # Mode detection (map or mat)
    if map_data['map_src'] is None and mat_data['mat_src'] is None:  # No reference points found
        ans = input('No mat or map source points have been found; do you have a mat (C)\n'
                    'or would you like to select these points directly from the map? (M) ')
        while True:
            if str(ans) == 'c' or str(ans) == 'C':
                mode = False
                break
            elif str(ans) == 'm' or str(ans) == 'M':
                mode = True
                break
            else:
                ans = input('Invalid input, try again:')

    elif isinstance(map_data['map_src'], np.ndarray) and mat_data['mat_src'] is None:  # Map reference points found
        mode = True
        print('Map reference points have been found.')
        if isinstance(map_data['map_dst'], np.ndarray):
            print('Map destination points have been found.')

    elif isinstance(mat_data['mat_src'], np.ndarray) and map_data['map_src'] is None:  # mat reference points found
        mode = False
        print('mat reference points have been found.')

    elif isinstance(map_data['map_src'], np.ndarray) and isinstance(mat_data['mat_src'], np.ndarray):  # Both map and mat reference points found
        ans = input('Both mat and map source points have been found;\n'
                    'would you like to create the map using the mat corners (C)\n'
                    'or the given map source points? (M) ')
        while True:
            if str(ans) == 'c' or str(ans) == 'C':
                mode = False
                break
            elif str(ans) == 'm' or str(ans) == 'M':
                mode = True
                if map_data['map_dst'] is not None:
                    print('')
                    print('Map destination points have been found.')
                break
            else:
                ans = input('Invalid input, try again:')

    else:
        print('An error occurred while reading the ' + setup_file + ', exiting program.')
        sys.exit(-1)

    print('')

    # Parameters
    if save is None:
        save = system_data['default_save']

    # Video stream loading
    cap = cv2.VideoCapture(src)  # 0 or -1 for default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file
    attempt = 0

    while not cap.isOpened() and attempt < system_data['max_attempts']:  # Check that the capture has been initialized
        cap.open()
        attempt += 1

    if not cap.isOpened() and attempt == system_data['max_attempts']:  # Exit if the capture has not been initialized after a number of attempts
        print('Could not open video stream. Exiting program...')
        sys.exit(-1)  # Exit program

    # Output video parameters
    if save:
        if dst_name is not None:
            output_video = dst_name.replace('.' + dst_name.partition('.')[len(dst_name.partition('.')) - 1], '.avi')  # Sets the specified name for the output video (replacing the original extension)...
        else:
            output_video = src[::-1].partition('.')[2].partition('/')[0][::-1] + '_output.avi'  # ...or just gets the input name and adds '_output.avi' at the end

        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Defines the codec and creates a VideoWriter object

        out = cv2.VideoWriter(output_video, fourcc, system_data['fps'], (int(cap.get(3)), int(cap.get(4))))
    else:
        out = None  # If the video is not to be saved, a null argument is passed

    # First frame processing
    process, map_ratio, points_p = process_frame_first(cap, src, out, mode, map_data, mat_data, overlay_data, status_bar_data, system_data['min_distance'])

    if not process:  # Exit program if process_first_frame() returns False
        print('An error occurred. Exiting program...')
        sys.exit()

    # Video processing
    while process:
        process, points_p = process_frame(cap, src, out, overlay_data, status_bar_data, system_data['min_distance'], map_ratio, system_data['position_alpha'], points_p)

    # Final operations
    cap.release()  # Release capture when finished

    if save:
        out.release()
        print('Video saved as ' + output_video + '.')
        print('')

    cv2.destroyAllWindows()  # Close window

    print('Exiting program...')
    sys.exit(0)  # Exit program


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(str(sys.argv[1]))
    if len(sys.argv) == 3:
        main(str(sys.argv[1]), sys.argv[2])
    if len(sys.argv) == 4:
        main(str(sys.argv[1]), sys.argv[2], sys.argv[3])
    if len(sys.argv) == 5:
        main(str(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('An error occurred in the ' + inspect.stack()[0][3] + ' function, exiting program.')
        sys.exit(-1)
