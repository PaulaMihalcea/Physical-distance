import cv2
import numpy as np
from get_distance import get_distance


def transform_coords(op_keypoints, h, warp_overlay_ratio, map_ratio, min_distance):

    if op_keypoints.shape:
        points = np.zeros((op_keypoints.shape[0], 2))

        for i in range(0, op_keypoints.shape[0]):
            points[i][0] = (op_keypoints[i][21][0] + op_keypoints[i][24][0]) / 2
            points[i][1] = (op_keypoints[i][21][1] + op_keypoints[i][24][1]) / 2
    else:
        points = None

    if points is not None and len(points) > 1:

        for i in range(0, len(points)):
            p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
            points[i][0] = int(p[0][0][0] / warp_overlay_ratio[0])
            points[i][1] = int(p[0][0][1] / warp_overlay_ratio[1])

        points = points.astype('int')

        distances = get_distance(points, map_ratio, min_distance)

    elif points is not None and len(points) == 1:
        for i in range(0, len(points)):
            p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
            points[i][0] = int(p[0][0][0] / warp_overlay_ratio[0])
            points[i][1] = int(p[0][0][1] / warp_overlay_ratio[1])

        points = points.astype('int')
        distances = None
    else:
        points = None
        distances = None

    return points, distances


def transform_coords_c(op_keypoints, h, warp_overlay_ratio, map_ratio, min_distance, warp_offset):

    if op_keypoints.shape:
        points = np.zeros((op_keypoints.shape[0], 2))

        for i in range(0, op_keypoints.shape[0]):
            points[i][0] = (op_keypoints[i][21][0] + op_keypoints[i][24][0]) / 2
            points[i][1] = (op_keypoints[i][21][1] + op_keypoints[i][24][1]) / 2
    else:
        points = None

    if points is not None and len(points) > 1:

        for i in range(0, len(points)):
            p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
            points[i][0] = int((p[0][0][0] - warp_offset[0]) / warp_overlay_ratio[0])
            points[i][1] = int((p[0][0][1] - warp_offset[1]) / warp_overlay_ratio[1])

        points = points.astype('int')

        distances = get_distance(points, map_ratio, min_distance)

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

    return points, distances
