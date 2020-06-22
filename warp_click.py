import cv2
import sys
import numpy as np
from utils import get_four_points
from get_dest_dim import get_dest_dim
from screeninfo import get_monitors


def warp(im_src, ratio, show=False):

    im_src = cv2.imread(im_src)  # Read source image

    pts_src = None

    while pts_src is None:


        ################# BORDER STUFF BEGINS ###################
        ans = input('Would you like to add a border? (Y/N) ')
        input_flag = False
        while input_flag is False:
            if ans is 'y' or ans is 'Y':
                border = [int(input('Insert left border thickness in pixels: ')), int(input('Insert top border thickness in pixels: ')), int(input('Insert right border thickness in pixels: ')), int(input('Insert bottom border thickness in pixels: '))]
                input_flag = True
                im_src = cv2.copyMakeBorder(im_src, border[1], border[3], border[0], border[2], cv2.BORDER_CONSTANT)  # Add border to image (for planes outside image)
            elif ans is 'n' or ans is 'N':
                input_flag = True
                pass
            else:
                ans = input('Invalid answer. Try again (Y/N): ')
        ################# BORDER STUFF ENDS ###################



        print('Click on the four points of the floor plane (top left, top right, bottom right, bottom left), then press ENTER.')

        cv2.imshow("Image", im_src)
        pts_src = get_four_points(im_src)

    dest_width, dest_height = get_dest_dim(pts_src, ratio)  # Calculate dimensions of destination image
    pts_dst = np.array([[0, 0], [dest_width - 1, 0], [dest_width - 1, dest_height - 1], [0, dest_height - 1]])

    h, status = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    im_out = np.zeros((im_src.shape[0], im_src.shape[1], 3), np.uint8)
    im_out = cv2.warpPerspective(im_src, h, (dest_width, dest_height))  # Warp source image based on homography

    ######################## DISPLAY INFO BEGINS ################################

    for m in get_monitors():
        info = str(m)
        display = info[info.find('DISPLAY1'):info.find('DISPLAY1')+8].strip()

    if display == 'DISPLAY1':
        display_width = int(info.split(',')[2].split('=')[1])
        display_height = int(info.split(',')[3].split('=')[1])

    display_tolerance = 50
    im_out_width = display_width - display_tolerance
    im_out_height = display_height - display_tolerance

    if im_out.shape[0] > im_out_width:
        y = int(im_out.shape[1] / (im_out.shape[0] / im_out_width))
        im_out = cv2.resize(im_out, (im_out_width, y))
    elif im_out.shape[1] > im_out_height:
        x = int(im_out.shape[0] / (im_out.shape[0] / im_out_height))
        im_out = cv2.resize(im_out, (x, im_out_height))

    ######################## DISPLAY INFO ENDS ################################



    cv2.imshow('', im_out)  # Display warped image
    cv2.waitKey(0)

    print('Warp complete.')

    return im_out

# TODO Delete tests below:

im_src = 'test/test_s_1.jpg'
im_src = 'test/stone.jpg'

ratio = 1
ratio = 9.3  # (stone)

warp(im_src, ratio, show=True)
