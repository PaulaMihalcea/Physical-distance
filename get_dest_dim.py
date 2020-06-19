import sys


def get_dest_dim(pts_src, ratio=1):
    x = []  # x coordinates of all points
    y = []  # y coordinates of all points

    for i in range(0, len(pts_src)):
        x.append(pts_src[i][0])
        y.append(pts_src[i][1])

    if ratio > 0:
        dest_width = int(max(x) - min(x))
        dest_height = int(int(max(y) - min(y)) * ratio)
    elif ratio < 0:
        dest_width = int(int(max(x) - min(x)) * ratio)
        dest_height = int(max(y) - min(y))
    else:
        print('Invalid ratio.')
        sys.exit(-1)

    return dest_width, dest_height
