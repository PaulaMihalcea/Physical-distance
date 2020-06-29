import numpy as np

def get_distance(points, map_dim):

    distances = np.zeros((len(points), len(points)))

    for i in range(0, len(points)):
        for j in range(0, len(points)):
            distances[i][j] = np.linalg.norm(points[i] - points[j])

    #print(distances)
    print(map_dim)

    return distances
