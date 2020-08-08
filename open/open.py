import cv2
import numpy as np  
import matplotlib.pyplot as plt

img = cv2.imread('b.jpg')
# opencv預設的imread是以BGR的方式進行儲存
InitImage = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

# 灰階影象處理
GrayImage = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# 高斯平滑
Gaussian = cv2.GaussianBlur(GrayImage, (3, 3), 0, 0, cv2.BORDER_DEFAULT)

# 中值濾波
Median = cv2.medianBlur(Gaussian, 5)

# Sobel運算元 XY方向求梯度
x = cv2.Sobel(Median, cv2.CV_8U, 1, 0, ksize = 3)
y = cv2.Sobel(Median, cv2.CV_8U, 0, 1, ksize = 3)
gradient = cv2.subtract(x, y)
Sobel = cv2.convertScaleAbs(gradient)

# 二值化（黑白）處理 周圍畫素影響
blurred = cv2.GaussianBlur(Sobel, (9, 9),0) #再進行一次高斯去噪
ret, Binary = cv2.threshold(Sobel, 170, 255, cv2.THRESH_BINARY)

# 膨脹和腐蝕操作的核函式
# element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
# # 膨脹一次, 讓輪廓突出
# Dilation = cv2.dilate(Binary, element2, iterations = 1)
# # 腐蝕一次, 去掉細節
# Erosion = cv2.erode(Dilation, element1, iterations = 1)
# # 再次膨脹, 讓輪廓明顯一些
# Dilation2 = cv2.dilate(Erosion, element2,iterations = 3)

# 建立一個橢圓核函式
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
# 執行影象形態學, 細節直接查文件
Dilation = cv2.morphologyEx(Binary, cv2.MORPH_CLOSE, kernel)
Erosion = cv2.erode(Dilation, None, iterations=4)
Dilation2 = cv2.dilate(Erosion, None, iterations=4)

# 輸出子圖
titles = ['Source Image', 'Gray Image', 'Gaussian Image', 'Median Image',
            'Sobel Image', 'Binary Image',
            'Dilation Image', 'Erosion Image', 'Dilation2 Image']
images = [InitImage, GrayImage, Gaussian, Median, Sobel, Binary,
            Dilation, Erosion, Dilation2]
for i in range(9):
   plt.subplot(4, 3, i+1) # (row, col, position)
   plt.imshow(images[i], 'gray')
   plt.title(titles[i])
   plt.xticks([])
   plt.yticks([])

plt.show()
cv2.waitKey(0)

# 使用Dilation2圖片確定車牌的輪廓
# https://blog.csdn.net/hjxu2016/article/details/77833336
contours, hierarchy = cv2.findContours(Dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
print('rectt', rect)
Box = np.int0(cv2.boxPoints(rect))
print('Box', Box)

# draw a bounding box arounded the detected barcode and display the image
Final_img = cv2.drawContours(img, [Box], -1, (0, 0, 255), 3)

cv2.imshow('Final_img', Final_img)
cv2.waitKey(0)