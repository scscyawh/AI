import cv2

img = cv2.imread(r"C:\Users\Hasee\Desktop\IMG_2951.JPG")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.bilateralFilter(img, 1, 75, 75)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img = cv2.Canny(img, 100, 200)
cv2.namedWindow('', flags=cv2.WINDOW_NORMAL)
cv2.resizeWindow('', 1600, 1000)
cv2.imshow('', img)
cv2.waitKey()