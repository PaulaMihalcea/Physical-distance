import numpy as np

def translate_homography(h, x_offset, y_offset):

    p = np.zeros((3, 3))

    p[0][0] = 1
    p[1][1] = 1
    p[2][2] = 1

    p[0][2] = - x_offset
    p[1][2] = - y_offset

    h = h.dot(p)

    return h









'''
# TODO: era tutto in utils

print(pts_src)  # TODO

# Select area around chessboard  # TODO
pts_src[0][0] = pts_src[0][0] - map_width_pixels
pts_src[0][1] = pts_src[0][1] - map_height_pixels

pts_src[1][0] = pts_src[1][0] + map_width_pixels
pts_src[1][1] = pts_src[1][1] - map_height_pixels

pts_src[2][0] = pts_src[2][0] + map_width_pixels
pts_src[2][1] = pts_src[2][1] + map_height_pixels

pts_src[3][0] = pts_src[3][0] - map_width_pixels
pts_src[3][1] = pts_src[3][1] + map_height_pixels


print()  # TODO
print(pts_src)  # TODO
'''
