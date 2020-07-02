import cv2
import numpy as np
from get_distance import get_distance


def transform_coord(points, h, warp_overlay_ratio, map_ratio, min_distance):

    for i in range(0, len(points)):
        p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
        points[i][0] = p[0][0][0] / warp_overlay_ratio[0]
        points[i][1] = p[0][0][1] / warp_overlay_ratio[1]

    distances = get_distance(points, map_ratio, min_distance)

    return points, distances
