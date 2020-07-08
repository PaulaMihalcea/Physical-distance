import cv2
import numpy as np
from get_dst_dim import get_dst_dim
import time

img_src = cv2.imread('test/test_c_s.jpg')

#cv2.imshow('', img)
#cv2.waitKey()

pts_src = np.float32([[109, 270], [138, 264], [153, 275], [123, 282]])  # angoli scacchiera test_C

qd = get_dst_dim(pts_src)
if qd[0] > qd[1]:
  q = qd[0]
else:
  q = qd[1]

pts_dst = np.array([[0, 0], [q, 0], [q, q], [0, q]])

h, _ = cv2.findHomography(pts_src, pts_dst)

height = img_src.shape[0]
width = img_src.shape[1]


roi_metri = 0.7  # da dare nelle impostazioni
roi = int(q * roi_metri * 100 / 30)


x = width * 10  # 1200
y = height * 10  # 1000

t = np.array([[1, 0, x],  # Dà lo spostamento a sx dalla scacchiera
                  [0, 1, y],  # Dà lo spostamento dall'alto della scacchiera
                  [0, 0, 1]],
                  dtype='float32')

#print(x, y)

th = t.dot(h)  # th = np.dot(t, h)

x2 = int(th[0][2]) * 10
y2 = int(th[1][2]) * 10

#print(x2, y2)

img_dst = cv2.warpPerspective(img_src, th, (x2, y2), borderValue=(255, 0, 0, 255))

################ inizio misura della posizione ###################
'''
start = time.time()

#p = np.float32([[[117, 260]]])
p = np.float32([[[128, 263]]])

pt = cv2.perspectiveTransform(p, th).astype('int')

img_dst = cv2.circle(img_dst, (pt[0][0][0], pt[0][0][1]), 3, (0, 255, 255, 255), -1)

end = time.time()

print('Tempo impiegato per misurare la posizione del punto:', end - start)
'''
################ fine misura della posizione ###################

#print('q:', q)

#print(img_dst.shape[1], img_dst.shape[0])

# crop
crop = 1

if crop == 1:
  img_dst = img_dst[y - roi : y + q + roi, x - roi: x + q + roi]
  #print(img_dst.shape[1], img_dst.shape[0])
else:
  factor = 2  # 25
  factor = img_dst.shape[0] / 500
  print('factor:', factor)
  dst_w = int(img_dst.shape[1] / factor)
  dst_h = int(img_dst.shape[0] / factor)
  dim = (dst_w, dst_h)
  img_dst = cv2.resize(img_dst, dim)

p = np.float32([[[128, 263]]])

pt = cv2.perspectiveTransform(p, th).astype('int')

pt[0][0][0] -= x - roi
pt[0][0][1] -= y - roi

print(pt)

img_dst = cv2.circle(img_dst, (pt[0][0][0], pt[0][0][1]), 3, (0, 255, 255, 255), -1)

#cv2.imwrite('ciao.jpg', img_dst)

cv2.imshow('', img_dst)
cv2.waitKey()
