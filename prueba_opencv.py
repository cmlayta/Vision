import cv2

img = cv2.imread("foto_python.jpg")

cv2.imshow("Imagen", img)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
