def adjust_position(points, add, dim_x, dim_y, tolerance):

    for k in range(0, len(points)):

        x = points[k][0] + add[0]
        y = points[k][1] + add[1]

        if x < dim_x[0]:
            if x < dim_x[0] - tolerance:
                points[k][0] = -10
            else:
                points[k][0] = dim_x[0]
        elif x > dim_x[1]:
            if x > dim_x[1] + tolerance:
                points[k][0] = -10
            else:
                points[k][0] = dim_x[1]
        else:
            points[k][0] = x

        if y < dim_y[0]:
            if y < dim_y[0] - tolerance:
                points[k][1] = -10
            else:
                points[k][1] = dim_y[0]
        elif y > dim_y[1]:
            if y > dim_y[1] + tolerance:
                points[k][1] = -10
            else:
                points[k][1] = dim_y[1]
        else:
            points[k][1] = y

    return points
