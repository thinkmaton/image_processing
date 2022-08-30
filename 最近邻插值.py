# -----------------------------------------
# description : 双线性插值
# author : thinkmaton
# date : 2022.8.30
# -----------------------------------------

import numpy as np
import cv2

def NearestNeighborInterpolation(src_image, zoom_ratio) :
    src_h, src_w = src_image.shape[0], src_image.shape[1]
    target_h, target_w = int(src_h * zoom_ratio), int(src_w * zoom_ratio)
    h_ratio, w_ratio = target_h / src_h, target_w / src_w
    target_image = np.zeros((target_h, target_w, 3))
    for target_x in range(target_h) : 
        for target_y in range(target_w) :
            x, y = target_x / h_ratio, target_y / w_ratio
            target_image[target_x][target_y] = src_image[min(int(x + 0.5), src_h - 1)][min(int(y + 0.5), src_w - 1)]   #四舍五入
    return target_image

def main() :
    src_image = cv2.imread('./image/bug.jpg')
    target_image = NearestNeighborInterpolation(src_image, 2)
    cv2.imwrite('./image/NNI_bug.jpg', target_image)
main()