import cv2
import numpy as np
from get_dest_dim import get_dest_dim

def unwarp(im_src, pts_src, show=False):

    im_src = cv2.imread(im_src)  # Read source image

    dest_width, dest_height = get_dest_dim(pts_src)  # Calculate dimensions of destination image

    pts_dst = np.array([[0, 0], [dest_width - 1, 0], [dest_width - 1, dest_height - 1], [0, dest_height - 1]])

    h, status = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (dest_width, dest_height))

    # Display images
    if show:
        cv2.imshow('', im_out)  # Display warped image

    cv2.waitKey(0)

    return im_out



# TODO Delete tests below:

im_src = 'test/test_s_1.jpg'
im_src = 'test/stone.jpg'

pts_src = np.array([[30, 373], [232, 373], [233, 473], [20, 477]])  # Four corners in source image (test_s_1)
pts_src = np.array([[214, 0], [417, 0], [625, 94], [0, 94]])  # Four corners in source image (stone)

unwarp(im_src, pts_src, show=True)
