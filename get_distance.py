import numpy as np


def get_distance(points, min_distance, map_ratio=1):

    if isinstance(map_ratio, str) or map_ratio is None:
        map_ratio = 1

    points = np.asmatrix(points, dtype='float64')
    points[:, 0] *= map_ratio[0]
    points[:, 1] *= map_ratio[1]

    distances = np.zeros((len(points), len(points)))

    for i in range(0, len(points)):
        for j in range(0, len(points)):
            distances[i][j] = np.linalg.norm(points[i] - points[j])

    v = []

    for i in range(0, len(distances)):
        for j in range(i + 1, len(distances)):
            if distances[i][j] < min_distance:
                v.append([i, j])
    if v:
        v = set(map(int, str(v).replace('[', ''). replace(']', '').split(', ')))

    return v
