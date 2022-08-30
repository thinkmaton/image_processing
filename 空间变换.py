# -----------------------------------------
# description : 逆仿射变换加插值实现图像空间变换
# author : thinkmaton
# created time : 2022.8.30 15:35
# -----------------------------------------
import math
from pickletools import TAKEN_FROM_ARGUMENT1
import cv2
import numpy as np

#invT为逆仿射变换矩阵
def NearestNeighborInterpolation(src_image, target_shape, invT) :
    src_h, src_w = src_image.shape[0], src_image.shape[1]
    target_h, target_w = target_shape
    target_image = np.zeros((target_h, target_w, 3))
    for target_x in range(target_h) : 
        for target_y in range(target_w) :
            target_vector = np.array([target_x, target_y, 1])
            src_vector = np.dot(target_vector, invT)
            x, y = src_vector[0], src_vector[1]
            target_image[target_x][target_y] = src_image[min(int(x + 0.5), src_h - 1)][min(int(y + 0.5), src_w - 1)]   #四舍五入
    return target_image

def doubleLinearInterpolation(src_image, target_shape, invT) :
    src_h, src_w = src_image.shape[0], src_image.shape[1]
    target_h, target_w = target_shape
    target_image = np.zeros((target_h, target_w, 3))    
    for target_x in range(target_h) : 
        for target_y in range(target_w) :
            target_vector = np.array([target_x, target_y, 1])
            src_vector = np.dot(target_vector, invT)
            x, y = src_vector[0], src_vector[1]
            x0, y0 = int(x), int(y)
            delta_x, delta_y = x - x0, y - y0
            left_up = src_image[x0][y0] * (1 - delta_x) * (1 - delta_y) if x0 < src_h and y0 < src_w else 0
            left_down = src_image[x0 + 1][y0] * delta_x * (1 - delta_y) if x0 + 1 < src_h and y0 < src_w else 0
            rigth_up = src_image[x0][y0 + 1] * (1 - delta_x) * delta_y if x0 < src_h and y0 + 1 < src_w else 0
            right_down = src_image[x0 + 1][y0 + 1] * delta_x * delta_y if x0 + 1 < src_h and y0 + 1 < src_w else 0
            target_image[target_x][target_y] = left_up + left_down + rigth_up + right_down
    return target_image

#缩放
#h_ratio, w_ratio 为缩放比例
def zoom(src_image, h_ratio, w_ratio) :
    src_h, src_w = src_image.shape[0], src_image.shape[1]
    target_shape = int(h_ratio * src_h), int(w_ratio * src_w)
    invT = np.array([[1 / h_ratio, 0, 0],
                     [0, 1 / w_ratio, 0],
                     [0, 0, 1]])
    return NearestNeighborInterpolation(src_image, target_shape, invT)

#旋转
#celta 为旋转的角度，方向为逆时针，需要顺时针旋转传入负角度即可
def rotate(src_image, celta) :
    src_h, src_w = src_image.shape[0], src_image.shape[1]
    target_shape = src_h, src_w
    center_x , center_y = (0 + src_h - 1) >> 1, (0 + src_w - 1) >> 1
    invT = np.array([[math.cos(celta), -math.sin(celta), 0],
                     [math.sin(celta), math.cos(celta), 0],
                     [center_x - (math.cos(celta) * center_x + math.sin(celta) * center_y),  center_y - (-math.sin(celta) * center_x + math.cos(celta) * center_y), 1]])
    return NearestNeighborInterpolation(src_image, target_shape, invT)

def main() : 
    src_image = cv2.imread('./image/bug.jpg')
    target_image, type_str = 0, 0
    print('1. zoom : ')
    print('2. rotate : ')
    opt = int(input('your choice : '))
    if opt == 1 : 
        h_ratio = float(input('h_ratio : '))
        w_ratio = float(input('w_ratio : '))
        target_image = zoom(src_image, h_ratio, w_ratio)
        type_str = 'zoom'
    if opt == 2 : 
        angle = float(input('rotate angle (counterclockwise) : '))
        target_image = rotate(src_image, angle / 180 * math.pi)
        type_str = 'rotate'
    cv2.imwrite('./image/' + type_str + '_bug.jpg', target_image)

main()