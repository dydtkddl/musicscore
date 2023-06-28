import cv2 
import numpy as np
img_path = "C:/users/admin/desktop/musicscore/images/"
detail_path = "bluewhale.pdf/bluewhale-2.jpg"
loaded_img = cv2.imread("%s%s"%(img_path, detail_path), cv2.IMREAD_GRAYSCALE)
# print(loaded_img.shape) -> (3509, 2481)
print(loaded_img.shape)

loaded_img = np.where(loaded_img>180,  0,255)
loaded_img = np.array(loaded_img, dtype=np.uint8)

for row in range(loaded_img.shape[0]):
    if np.count_nonzero(loaded_img[row])< loaded_img.shape[1]*0.7:
        pass
    else:
        loaded_img[row] = 0
loaded_img = cv2.morphologyEx(loaded_img, cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
label_info = cv2.connectedComponentsWithStats(loaded_img, 4)
stats = label_info[2]
for i,stat in enumerate(stats):
    print(i)
    x = stat[0]
    y = stat[1]
    width = stat[2]
    height = stat[3]
    cv2.imwrite("images/objects/object_%sth.jpg"%i,loaded_img[y:y+height, x:x+width])
winname = "window"
width = int(loaded_img.shape[0]/3)
height =  int(loaded_img.shape[1]/2)
cv2.namedWindow(winname, flags=cv2.WINDOW_NORMAL)
cv2.imshow(winname , loaded_img)
cv2.resizeWindow(winname, width, height )
while True:
    if cv2.waitKey(delay=None) == ord('q'): 
        break
    if cv2.waitKey(delay=None) == ord('s'):
        cv2.imwrite("img.jpg",loaded_img)
cv2.destroyWindow(winname)