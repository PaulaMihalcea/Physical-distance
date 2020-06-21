import cv2
import numpy as np
from get_dest_dim import get_dest_dim


def warp(im_src, pts_src, ratio, border=[0, 0, 0, 0], show=False):

    im_src = cv2.imread(im_src)  # Read source image
    im_src = cv2.copyMakeBorder(im_src, border[0], border[1], border[2], border[3], cv2.BORDER_CONSTANT)  # Add border to image (for planes outside image)

    dest_width, dest_height = get_dest_dim(pts_src, ratio)  # Calculate dimensions of destination image

    pts_dst = np.array([[0, 0], [dest_width - 1, 0], [dest_width - 1, dest_height - 1], [0, dest_height - 1]])

    h, status = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    im_out = np.zeros(im_src.shape)
    im_out = cv2.warpPerspective(im_src, h, (dest_width, dest_height))  # Warp source image based on homography

    if show:
        # cv2.imshow('', im_src)  # Display source image
        cv2.imshow('', im_out)  # Display warped image
    cv2.waitKey(0)

    return im_out



# TODO Delete tests below:

im_src = 'test/test_s_1.jpg'
im_src = 'test/stone.jpg'

pts_src = np.array([[30, 373], [232, 373], [233, 473], [20, 477]])  # Four corners in source image (test_s_1)
pts_src = np.array([[51, 373], [136, 373], [236, 473], [23, 477]])  # Four corners in source image (test_s_1 modificato)

# Rapporto x/y per correggere l'altezza dell'immagine in modo da ottenere una vista dall'alto
ratio = 1
ratio = 9.3  # (stone)

b = 100

border = [b, b, b, b]

pts_src = np.array([[214+b, 0+b], [417+b, 0+b], [625+b, 94+b], [0+b, 94+b]])  # Four corners in source image (stone)

warp(im_src, pts_src, ratio, border, show=True)
