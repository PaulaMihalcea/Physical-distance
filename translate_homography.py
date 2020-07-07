import cv2
import numpy as np

def translate_homography(img_src, pts_src, pts_dst):

    #img_src = cv2.imread('test/test_c_frame.png')  # TODO

    # pts_src = np.array([[100, 100], [200, 100], [200, 200], [100, 200]])  # TODO
    #pts_dst = np.array([[0, 0], [100, 0], [100, 150], [0, 230]])  # TODO

    h, _ = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

    print(pts_dst)

    width = img_src.shape[1]
    height = img_src.shape[0]

    corners = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])

    corners = cv2.perspectiveTransform(np.float32([corners]), h)[0]

    print(corners)
    print()
    print()
    '''
    print(corners)

    points = np.copy(corners)

    for i in range(0, len(points)):
        p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
        points[i][0] = int(p[0][0][0])
        points[i][1] = int(p[0][0][1])
    
    '''
    bx, by, bwidth, bheight = cv2.boundingRect(corners)

    # print(points)

    print(bx, by, bwidth, bheight)
    print()


    ###############################

    th = dot(h, bx, by)
    '''
    points = corners

    for i in range(0, len(points)):
        p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), th).astype('int')
        points[i][0] = int(p[0][0][0])
        points[i][1] = int(p[0][0][1])

    #print()
    print(points)
    
    
    
    bx, by, bwidth, bheight = cv2.boundingRect(points)

    print(bx, by, bwidth, bheight)
    '''


    warped = cv2.warpPerspective(img_src, th, (bwidth, bheight))
    warped = cv2.resize(warped, (270, 480))

    cv2.imshow('', warped)
    cv2.waitKey()

    return warped


def dot_c(h, x_offset, y_offset):

    t = np.zeros((3, 3))

    t[0][0] = 1
    t[1][1] = 1
    t[2][2] = 1

    t[0][2] = - x_offset
    t[1][2] = - y_offset

    h = t.dot(h)

    return h








'''
# TODO: era tutto in utils

print(pts_src)  # TODO

# Select area around chessboard  # TODO
pts_src[0][0] = pts_src[0][0] - map_width_pixels
pts_src[0][1] = pts_src[0][1] - map_height_pixels

pts_src[1][0] = pts_src[1][0] + map_width_pixels
pts_src[1][1] = pts_src[1][1] - map_height_pixels

pts_src[2][0] = pts_src[2][0] + map_width_pixels
pts_src[2][1] = pts_src[2][1] + map_height_pixels

pts_src[3][0] = pts_src[3][0] - map_width_pixels
pts_src[3][1] = pts_src[3][1] + map_height_pixels


print()  # TODO
print(pts_src)  # TODO
'''
