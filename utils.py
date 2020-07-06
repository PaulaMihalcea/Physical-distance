import cv2
import sys
import numpy as np
from configparser import ConfigParser
from get_dst_dim import get_dst_dim, get_dst_dim_chessboard


def is_int(n):
    try:
        n = int(n)
        return n
    except ValueError:
        return None


def get_points_mouse(img_src, pts_dst):

    # Variables
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    ratio = f.getfloat('General', 'ratio')

    pts_src = None  # Source points
    img_src_b = img_src.copy()  # Image with border

    # Get points by click
    while True:  # Wait for four valid source points

        print('Click on the four corners of the floor plane (top left, top right, bottom right, bottom left) then press ENTER,\n'
              'or press SPACEBAR to add or change borders.\n'
              'Otherwise, press ESC to exit.')
        print('')

        pts_src = get_pts(img_src_b)

        if pts_src is not None:  # Exit source points loop if four valid points have been returned
            break
        else:
            border = [None] * 4  # Border thickness
            while True:
                border[0] = is_int(input('Insert left border thickness in pixels: '))
                if border[0] is None or border[0] < 0:
                    print('Invalid input.')
                else:
                    break
            while True:
                border[1] = is_int(input('Insert top border thickness in pixels: '))
                if border[1] is None or border[1] < 0:
                    print('Invalid input.')
                else:
                    break
            while True:
                border[2] = is_int(input('Insert right border thickness in pixels: '))
                if border[2] is None or border[2] < 0:
                    print('Invalid input.')
                else:
                    break
            while True:
                border[3] = is_int(input('Insert bottom border thickness in pixels: '))
                if border[3] is None or border[3] < 0:
                    print('Invalid input.')
                else:
                    break

            print('')
            img_src_b = cv2.copyMakeBorder(img_src, border[1], border[3], border[0], border[2], cv2.BORDER_CONSTANT)  # Add border to image (for planes outside image)

    # Get destination points
    if pts_dst is None:
        dst_width, dst_height = get_dst_dim(pts_src, ratio)  # Calculate dimensions of destination image
        pts_dst = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]])  # Set destination points
    else:
        dst_width, dst_height = get_dst_dim(pts_dst, ratio)  # Calculate dimensions of destination image
        dst_width += 1
        dst_height += 1

    return pts_src, pts_dst, (dst_width, dst_height)


def get_points_chessboard(img_src, pts_src, pts_dst):

    # Variables
    f = ConfigParser()
    f.read('setup.ini')  # Parse the setup.ini file to retrieve settings

    ratio = f.getfloat('General', 'ratio')
    map_width_pixels = f.getint('General', 'map_width_pixels')
    map_height_pixels = f.getint('General', 'map_height_pixels')

    img_src_b = img_src.copy()  # Image with border

    # Get points by click

    print('Click on the four corners of the chessboard (top left, top right, bottom right, bottom left) the press ENTER.\n'
          'Otherwise, press ESC to exit.')
    print('')

    if pts_src is None:
        pts_src = get_pts_no_borders(img_src_b)

    # Get destination points
    if pts_dst is None:
        dst_width, dst_height = get_dst_dim_chessboard(pts_src, ratio)  # Calculate dimensions of destination image
        pts_dst = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]])  # Set destination points
    else:
        dst_width, dst_height = get_dst_dim(pts_dst, ratio)  # Calculate dimensions of destination image
        dst_width += 1
        dst_height += 1

    return pts_src, pts_dst, (dst_width, dst_height)


def get_color(n):  # Choose a color based on the number of the point that is about to be drawn

    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]  # The first four points are (in order) red, green, blue and yellow; other points will be invisible and not considered

    if n == 0:
        c = colors[0]
    elif n == 1:
        c = colors[1]
    elif n == 2:
        c = colors[2]
    elif n == 3:
        c = colors[3]
    else:
        c = (0, 0, 0, 0)

    return c


def mouse_handler(event, x, y, flags, data):

    if event == cv2.EVENT_LBUTTONDOWN and len(data['pts']) < 4:
        c = get_color(len(data['pts']))  # Get the color of the point that is about to be drawn on the image
        cv2.circle(data['img'], (x, y), 5, c, -1)  # Draw a small dot of the selected color centered around the pixel the user has clicked on
        cv2.imshow('Choose points...', data['img'])  # Show the original image
        data['pts'].append([x, y])  # Append the acquired point to the points array


def get_pts(im):

    data = {'img': im.copy(),  # Use a copy of the original image during the points' acquisition
            'pts': []}  # Array of points
    cv2.imshow('Choose points...', data['img'])  # Show the image to choose points on

    while True:

        cv2.setMouseCallback('Choose points...', mouse_handler, data)  # Set the callback function for any mouse event
        k = cv2.waitKey(0)  # Get whatever key the user presses on keyboard

        if k == 13 and len(data['pts']) == 4:  # ENTER is pressed and all four points have been acquired
            cv2.destroyAllWindows()  # Close the choosing points window and return
            break
        if k == 32:  # SPACEBAR
            cv2.destroyAllWindows()  # Close the choosing points window and return the necessary flags to begin a new operation
            return None
        if k == 27:  # ESC
            print('Exiting program...')
            sys.exit()  # Exit program
        else:  # Any other key
            print('Invalid key or not enough points selected (points left: ' + str(4 - len(data['pts'])) + '). Press ENTER to continue.')
            print('')

    pts = np.vstack(data['pts']).astype(float)  # Convert points array to a numpy array
    
    return pts


def get_pts_no_borders(im):

    data = {'img': im.copy(),  # Use a copy of the original image during the points' acquisition
            'pts': []}  # Array of points
    cv2.imshow('Choose points...', data['img'])  # Show the image to choose points on

    while True:

        cv2.setMouseCallback('Choose points...', mouse_handler, data)  # Set the callback function for any mouse event
        k = cv2.waitKey(0)  # Get whatever key the user presses on keyboard

        if k == 13 and len(data['pts']) == 4:  # ENTER is pressed and all four points have been acquired
            cv2.destroyAllWindows()  # Close the choosing points window and return
            break
        if k == 27:  # ESC
            print('Exiting program...')
            sys.exit()  # Exit program
        else:  # Any other key
            print('Invalid key or not enough points selected (points left: ' + str(4 - len(data['pts'])) + '). Press ENTER to continue.')
            print('')

    pts = np.vstack(data['pts']).astype(float)  # Convert points array to a numpy array

    return pts
