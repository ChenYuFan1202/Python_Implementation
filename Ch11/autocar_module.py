#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cv2
import numpy as np

def get_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 灰階處理
    blur = cv2.GaussianBlur(gray, (13, 13), 0) # 高斯模糊
    canny = cv2.Canny(blur, 50, 150) # 邊緣偵測
    return canny

def get_roi(img):
    mask = np.zeros_like(img) # 全黑遮罩
    points = np.array([[[146, 539],  # 建立多邊形座標
                        [781, 539],
                        [515, 417],
                        [296, 397]]])
    cv2.fillPoly(mask, points, 255) # 多邊三角形
    roi = cv2.bitwise_and(img, mask)
    return roi

def draw_lines(img, lines):
    for line in lines:
        points = line.reshape(4, )
        x1, y1, x2, y2 = points
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
    return img

def get_avglines(lines):
    if lines is None:
        print("偵測不到直線線段")
        return None
    
    lefts = []
    rights = []
    for line in lines:
        points = line.reshape(4, )
        x1, y1, x2, y2 = points
        slope, b = np.polyfit((x1, x2), (y1, y2), deg = 1)
        if slope > 0:
            rights.append([slope, b])
        else:
            lefts.append([slope, b])
            
    if rights and lefts:
        right_avg = np.average(rights, axis = 0)
        left_avg = np.average(lefts, axis = 0)
        return np.array([right_avg, left_avg])
    else:
        print("無法同時偵測到左右邊線")
        return None
    
def get_sublines(img, avglines):
    sublines = []
    for line in avglines:
        slope, b = line
        y1 = img.shape[0]
        y2 = int(y1 * (3 / 5))
        x1 = int((y1 - b) / slope)
        x2 = int((y2 - b) / slope)
        sublines.append([x1, y1, x2, y2])
    return np.array(sublines)