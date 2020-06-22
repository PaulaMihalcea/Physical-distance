import cv2
import numpy as np


def mouse_handler(event, x, y, flags, data) :
    
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(data['im'], (x,y),3, (0,0,255), 5, 16)
        cv2.imshow("Image", data['im'])

        if len(data['points']) < 4:
            data['points'].append([x,y])


def get_four_points(im):
    
    # Set up data to send to mouse handler
    data = {'im': im.copy(),
            'points': []}
    
    # Set the callback function for any mouse event
    while True:
        for i in range(0, len(data['points'])):
            data['im'] = cv2.circle(data['im'], (data['points'][i][0], data['points'][i][1]), 3, (0, 0, 255), 5, 16)  # TODO

        cv2.setMouseCallback("Image", mouse_handler, data)

        k = cv2.waitKey(0)

        if k == 13 and len(data['points']) == 4:  # ENTER
            cv2.destroyAllWindows()
            break
        if k == 32:
            print('SPACER pressed')
            return
        else:
            cv2.imshow("Image", data['im'])
            print('Invalid key or not enough points selected (points left: ' + str(4 - len(data['points'])) + '). Press ENTER to continue.')
    
    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)
    print(type(points))
    
    return points
