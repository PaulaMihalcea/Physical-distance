import cv2
import numpy as np
import sys
from read_ini import read_ini
from process_frame import process_frame_first, process_frame


def main(src, setup_file, save=None, dst_name=None):

    print('')
    print('Welcome to the Physical Distance Detector!')
    print('')

    # Setup
    system, map_data, chessboard_data, overlay_data, status_bar_data = read_ini(setup_file)
    mode = None  # If True, map reference points of that type have been found; if False, chessboard reference points have been found

    # Mode detection (map or chessboard)
    if map_data['map_src'] is None and chessboard_data['chessboard_src'] is None:  # No reference points found
        ans = input('No chessboard or map source points have been found; do you have a chessboard (C)\n'
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

    elif isinstance(map_data['map_src'], np.ndarray) and chessboard_data['chessboard_src'] is None:  # Map reference points found
        mode = True
        print('Map reference points have been found.')
        if isinstance(map_data['map_dst'], np.ndarray):
            print('Map destination points have been found.')

    elif isinstance(chessboard_data['chessboard_src'], np.ndarray) and map_data['map_src'] is None:  # Chessboard reference points found
        mode = False
        print('Chessboard reference points have been found.')

    elif isinstance(map_data['map_src'], np.ndarray) and isinstance(chessboard_data['chessboard_src'], np.ndarray):  # Both map and chessboard reference points found
        ans = input('Both chessboard and map source points have been found;\n'
                    'would you like to create the map using the chessboard corners (C)\n'
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
        save = system['default_save']

    status_text = [[[status_bar_data['status_1'], status_bar_data['status_1_color'], status_bar_data['status_1_offset'], status_bar_data['line_spacing_1']],
                    [status_bar_data['status_2'], status_bar_data['status_2_color'], status_bar_data['status_2_offset'], status_bar_data['line_spacing_2']],
                    [status_bar_data['status_3'], status_bar_data['status_3_color'], status_bar_data['status_3_offset'], status_bar_data['line_spacing_3']]],

                   [[status_bar_data['status_1_alt'], status_bar_data['status_1_color_alt'], status_bar_data['status_1_offset_alt'], status_bar_data['line_spacing_1_alt']],
                    [status_bar_data['status_2_alt'], status_bar_data['status_2_color_alt'], status_bar_data['status_2_offset_alt'], status_bar_data['line_spacing_2_alt']],
                    [status_bar_data['status_3_alt'], status_bar_data['status_3_color_alt'], status_bar_data['status_3_offset_alt'], status_bar_data['line_spacing_3_alt']]]]

    # Video stream loading
    cap = cv2.VideoCapture(src)  # 0 or -1 for default camera, 1 for next one and so on; passing a string containing a path/filename opens an external video file
    attempt = 0

    while not cap.isOpened() and attempt < system['max_attempts']:  # Check that the capture has been initialized
        cap.open()
        attempt += 1

    if not cap.isOpened() and attempt == system['max_attempts']:  # Exit if the capture has not been initialized after a number of attempts
        print('Could not open video stream. Exiting program...')
        sys.exit(-1)  # Exit program

    # Output video parameters
    if save:
        if dst_name is not None:
            output_video = dst_name.replace('.' + dst_name.partition('.')[len(dst_name.partition('.')) - 1], '.avi')  # Sets the specified name for the output video (replacing the original extension)...
        else:
            output_video = src[::-1].partition('.')[2].partition('/')[0][::-1] + '_output.avi'  # ...or just gets the input name and adds '_output.avi' at the end

        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Defines the codec and creates a VideoWriter object

        out = cv2.VideoWriter(output_video, fourcc, system['fps'], (int(cap.get(3)), int(cap.get(4))))
    else:
        out = None  # If the video is not to be saved, a null argument is passed

    # First frame processing
    process, map_ratio = process_frame_first(cap, src, out, mode, map_data, chessboard_data, overlay_data, [status_bar_data, status_text], system['min_distance'])

    if not process:  # Exit program if process_first_frame() returns False
        print('An error occurred or the user closed the window. Exiting program...')
        sys.exit()

    # Video processing
    while process:
        process = process_frame(cap, src, out, overlay_data, [status_bar_data, status_text], system['min_distance'], map_ratio)

    # Final operations
    cap.release()  # Release capture when finished

    if save:
        out.release()
        print('Video saved as ' + output_video + '.')
        print('')

    cv2.destroyAllWindows()  # Close window

    print('Exiting program...')
    sys.exit(0)  # Exit program


'''  # TODO aggiorna coi nuovi parametri
if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        main(str(sys.argv[1]))
    if len(sys.argv) == 3:
        main(str(sys.argv[1]), sys.argv[2])
    if len(sys.argv) == 4:
        main(str(sys.argv[1]), sys.argv[2], sys.argv[3])
'''

src = 'test/test_s.mp4'
#src = 'test/test_c.mp4'
#src = 'test/test_c_2.mp4'
#chessboard = False
save = False
setup = 'setup_r.ini'
setup = 'setup_c.ini'
#setup = 'setup_c_2.ini'
setup = 'setup.ini'

main(src, setup, save, 'test_c_2_openpose.avi')
