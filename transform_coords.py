import cv2
import numpy as np
from get_distance import get_distance


def transform_coords(op_keypoints, h, warp_overlay_ratio, map_ratio, min_distance, warp_offset, alpha=None, points_p=None):

    if op_keypoints.shape:
        points = np.zeros((op_keypoints.shape[0], 2))

        for i in range(0, op_keypoints.shape[0]):
            points[i][0] = (op_keypoints[i][21][0] + op_keypoints[i][24][0]) / 2
            points[i][1] = (op_keypoints[i][21][1] + op_keypoints[i][24][1]) / 2

    else:
        points = None

    if warp_offset is None:
        warp_offset = [0, 0]

    if points is not None and len(points) > 1:
        for i in range(0, len(points)):
            p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
            points[i][0] = int((p[0][0][0] - warp_offset[0]) / warp_overlay_ratio[0])
            points[i][1] = int((p[0][0][1] - warp_offset[1]) / warp_overlay_ratio[1])

        points = points.astype('int')

        distances = get_distance(points, min_distance, map_ratio)

    elif points is not None and len(points) == 1:
        for i in range(0, len(points)):
            p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
            points[i][0] = int((p[0][0][0] - warp_offset[0]) / warp_overlay_ratio[0])
            points[i][1] = int((p[0][0][1] - warp_offset[1]) / warp_overlay_ratio[1])

        points = points.astype('int')
        distances = None
    else:
        points = None
        distances = None

    if (points is not None) and (points_p is not None) and (len(points) == len(points_p)):
        for i in range(0, len(points)):
            points[i][0] = points[i][0] * alpha + points_p[i][0] * (1 - alpha)
            points[i][1] = points[i][1] * alpha + points_p[i][1] * (1 - alpha)

    if points is not None:
        points_p = points.copy()

    return points, distances, points_p


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
