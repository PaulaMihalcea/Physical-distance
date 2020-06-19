def get_dest_dim(pts_src):
    x = []  # x coordinates of all points
    y = []  # y coordinates of all points

    for i in range(0, len(pts_src)):
        x.append(pts_src[i][0])
        y.append(pts_src[i][1])

    dest_width = max(x) - min(x)
    dest_height = max(y) - min(y)

    return dest_width, dest_height
