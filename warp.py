import cv2
import numpy as np
from get_dest_dim import get_dest_dim
from screeninfo import get_monitors
from utils import get_points


def warp(im_src, src_type, ratio, show=False):  # TODO src_type

    im_src = cv2.imread(im_src)  # Read source image
    pts_src = []  # Source points

    # BORDERS

    ans = input('Would you like to add a border? (Y/N) ')  # Ask the user if borders are needed

    while True:  # Wait for four valid source points
        while True:  # Wait for user input

            if ans is 'y' or ans is 'Y' or pts_src is None:  # Borders needed
                print('')
                border = [int(input('Insert left border thickness in pixels: ')), int(input('Insert top border thickness in pixels: ')), int(input('Insert right border thickness in pixels: ')), int(input('Insert bottom border thickness in pixels: '))]  # Get border thickness
                print('')
                im_src_b = cv2.copyMakeBorder(im_src, border[1], border[3], border[0], border[2], cv2.BORDER_CONSTANT)  # Add border to image (for planes outside image)
                break  # Exit input loop

            elif ans is 'n' or ans is 'N':  # No borders needed
                im_src_b = im_src.copy()
                break  # Exit input loop

            else:  # Wrong input; keep waiting for input
                ans = input('Invalid answer. Try again (Y/N): ')

        print('')
        print('Click on the four points of the floor plane (top left, top right, bottom right, bottom left) then press ENTER,\n'
              'or press SPACEBAR to go back and add or change borders.')
        print('')

        pts_src = get_points(im_src_b)

        if pts_src is not None:  # Exit source points loop if four valid points have been returned
            break

    # WARP

    dest_width, dest_height = get_dest_dim(pts_src, ratio)  # Calculate dimensions of destination image
    pts_dst = np.array([[0, 0], [dest_width - 1, 0], [dest_width - 1, dest_height - 1], [0, dest_height - 1]])  # Set destination points

    h, status = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    im_out = np.zeros((im_src.shape[0], im_src.shape[1], 3), np.uint8)  # Create output image
    im_out = cv2.warpPerspective(im_src, h, (dest_width, dest_height))  # Warp source image based on homography

    # DISPLAY RESOLUTION

    display = []  # Monitor info list

    for m in get_monitors():  # Cycle on monitors found by the screeninfo library
        info = str(m)
        display.append(info[info.find('DISPLAY1'):info.find('DISPLAY1')+8].strip())  # Get monitor name

    for i in range(0, len(display)):  # Get width and height of main monitor; it is assumed to be the first that appears in the list
        if display[i] == 'DISPLAY1':
            display_width = int(info.split(',')[2].split('=')[1])
            display_height = int(info.split(',')[3].split('=')[1])

    display_tolerance = 50  # If the warped image is too large, an amount of pixels equal to this number will be left around the image window, so as to avoid occupying the whole screen
    im_out_width = display_width - display_tolerance
    im_out_height = display_height - display_tolerance

    if im_out.shape[0] > im_out_width:  # Resize warped image window if its width is larger than the screen width
        y = int(im_out.shape[1] / (im_out.shape[0] / im_out_width))
        im_out = cv2.resize(im_out, (im_out_width, y))
    elif im_out.shape[1] > im_out_height:  # Resize warped image window if its height is larger than the screen height
        x = int(im_out.shape[0] / (im_out.shape[0] / im_out_height))
        im_out = cv2.resize(im_out, (x, im_out_height))

    cv2.imshow('', im_out)  # Display warped image
    cv2.waitKey(0)

    return im_out

# TODO Delete tests below:


im_src = 'test/test_s_1.jpg'
im_src = 'test/stone.jpg'

ratio = 1
ratio = 9.3  # (stone)

src_type = 'image'

warp(im_src, src_type, ratio, show=True)

