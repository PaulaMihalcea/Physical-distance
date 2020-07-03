import cv2
import numpy as np
from get_distance import get_distance


def transform_coord(points, h, warp_overlay_ratio, map_ratio, min_distance):

    #print(points)

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
