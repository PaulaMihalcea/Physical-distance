import cv2
import numpy as np

def transform_coord(points, h, warp_overlay_ratio):

    p = []

    for i in range(0, len(points)):
        p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
        points[i][0] = p[0][0][0] / warp_overlay_ratio[0]
        points[i][1] = p[0][0][1] / warp_overlay_ratio[1]

    return points
