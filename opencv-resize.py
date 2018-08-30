import cv2
# for test in face net train
for i in range(10):
    name = "face_{}.png".format(i)
    img = cv2.imread(name)
    img = cv2.resize(img,(85,100))
    cv2.imwrite(name,img)


