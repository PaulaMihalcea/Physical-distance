import cv2
import sys
import numpy as np


def get_color(n):  # Choose a color based on the number of the point that is about to be drawn

    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]  # The first four points are (in order) red, green, blue and yellow; other points will be invisible

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
            sys.exit()  # Exit the whole program
        else:  # Any other key
            print('Invalid key or not enough points selected (points left: ' + str(4 - len(data['pts'])) + '). Press ENTER to continue.')
            print('')

    pts = np.vstack(data['pts']).astype(float)  # Convert points array to a numpy array
    
    return pts
