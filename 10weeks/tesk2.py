import cv2 as cv
import numpy as np

img1 = cv.imread('1.jpg')
img2 = cv.imread('2.jpg')
img3 = cv.imread('3.jpg')
img4 = cv.imread('4.jpg')
print(np.shape(img1))

# 노란색 라인 감지
lower_yellow_rgb = np.array([0, 180, 180])    # 노랑 최소치
upper_yellow_rgb = np.array([90, 255, 255])  # 노랑 최대치

print(np.shape(lower_yellow_rgb))

# cv2.inRange로 범위의 값만 마스크 생성
mask_yellow1 = cv.inRange(img1, lower_yellow_rgb, upper_yellow_rgb)
mask_yellow2 = cv.inRange(img2, lower_yellow_rgb, upper_yellow_rgb)
mask_yellow3 = cv.inRange(img3, lower_yellow_rgb, upper_yellow_rgb)
mask_yellow4 = cv.inRange(img4, lower_yellow_rgb, upper_yellow_rgb)

#원본 영상에 마스크를 씌워 필터링
final_yellow1 = cv.bitwise_and(img1,img1, mask=mask_yellow1)
final_yellow2 = cv.bitwise_and(img2,img2, mask=mask_yellow2)
final_yellow3 = cv.bitwise_and(img3,img3, mask=mask_yellow3)
final_yellow4 = cv.bitwise_and(img4,img4, mask=mask_yellow4)

cv.imshow("1",final_yellow1)
cv.imshow("2",final_yellow2)
cv.imshow("3",final_yellow3)
cv.imshow("4",final_yellow4)
cv.imwrite('yellow_img1.jpg',final_yellow1)
cv.imwrite('yellow_img2.jpg',final_yellow2)
cv.imwrite('yellow_img3.jpg',final_yellow3)
cv.imwrite('yellow_img4.jpg',final_yellow4)

cv.waitKey(0)
cv.destroyAllWindows()