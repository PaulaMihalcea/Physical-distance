import sys
import inspect


def get_dim(pts, mode, ratio=1):
    x = []  # x coordinates of all points
    y = []  # y coordinates of all points

    for i in range(0, len(pts)):
        x.append(pts[i][0])
        y.append(pts[i][1])

    if mode:  # Map
        if ratio > 0:
            dst_width = int(max(x) - min(x))
            dst_height = int(int(max(y) - min(y)) * ratio)
        elif ratio < 0:
            dst_width = int(int(max(x) - min(x)) * ratio)
            dst_height = int(max(y) - min(y))
        else:
            print('Invalid map ratio given to the ' + inspect.stack()[0][3] + ' function, exiting program.')
            sys.exit(-1)

    elif not mode:  # Chessboard
        dst_width = int(max(x) - min(x))
        dst_height = int(max(y) - min(y))

        if dst_width > dst_height:
            dst_height = dst_width
        elif dst_height > dst_width:
            dst_width = dst_height

        dst_width -= 1
        dst_height -= 1

    else:  # Shouldn't even get to this point, but whatever
        print('An error occurred in the ' + inspect.stack()[0][3] + ' function, exiting program.')
        sys.exit(-1)

    return dst_width, dst_height
