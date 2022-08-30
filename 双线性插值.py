# -----------------------------------------
# description : 双线性插值
# author : thinkmaton
# date : 2022.8.30
# -----------------------------------------

from audioop import ratecv
from ctypes.wintypes import tagRECT
import numpy as np
import cv2

eps = 1e-5

def doubleLinearInterpolation(src_image, zoom_ratio) :
    src_h, src_w = src_image.shape[0], src_image.shape[1]
    target_h, target_w = int(src_h * zoom_ratio), int(src_w * zoom_ratio)
    h_ratio, w_ratto = target_h / src_h, target_w / src_w
    print(target_h)
    print(target_w)
    target_image = np.zeros((target_h, target_w, 3))
    for target_x in range(target_h) : 
        for target_y in range(target_w) :
            x, y = target_x / h_ratio, target_y / w_ratto
            x0, y0 = int(x), int(y)
            delta_x, delta_y = x - x0, y - y0
            left_up = src_image[x0][y0] * (1 - delta_x) * (1 - delta_y) 
            left_down = src_image[x0 + 1][y0] * delta_x * (1 - delta_y) if x0 + 1 < src_h else 0
            rigth_up = src_image[x0][y0 + 1] * (1 - delta_x) * delta_y if y0 + 1 < src_w else 0
            right_down = src_image[x0 + 1][y0 + 1] * delta_x * delta_y if x0 + 1 < src_h and y0 + 1 < src_w else 0
            target_image[target_x][target_y] = left_up + left_down + rigth_up + right_down
    return target_image

def main() :
    src_image = cv2.imread('./image/bug.jpg')
    target_image = doubleLinearInterpolation(src_image, 1.5)
    cv2.imwrite('./image/big_bug.jpg', target_image)
main()