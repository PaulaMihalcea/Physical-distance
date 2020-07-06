import cv2
import numpy as np
from translate_homography import translate_homography

img_src = cv2.imread('test/test_c_frame.png')

pts_src = np.array([[100, 100], [200, 100], [200, 200], [100, 200]])

pts_dst = np.array([[0, 0], [100, 0], [100, 150], [0, 230]])

h, _ = cv2.findHomography(pts_src, pts_dst)  # Calculate homography

width = img_src.shape[1]
height = img_src.shape[0]

corners = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])

points = np.copy(corners)

for i in range(0, len(points)):
    p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), h).astype('int')
    points[i][0] = int(p[0][0][0])
    points[i][1] = int(p[0][0][1])

#print(points)

bx, by, bwidth, bheight = cv2.boundingRect(points)

#print(bx, by, bwidth, bheight)


###############################


th = translate_homography(h, bx, by)

points = corners

for i in range(0, len(points)):
    p = cv2.perspectiveTransform(np.array([[[points[i][0], points[i][1]]]], dtype='float32'), th).astype('int')
    points[i][0] = int(p[0][0][0])
    points[i][1] = int(p[0][0][1])

print()
print(points)

bx, by, bwidth, bheight = cv2.boundingRect(points)

print(bx, by, bwidth, bheight)


warped = cv2.warpPerspective(img_src, th, (bwidth, bheight))
warped = cv2.resize(warped, (270, 480))

cv2.imshow('', warped)
cv2.waitKey()

