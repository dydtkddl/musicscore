import cv2
img=cv2.imread("musicscore/images/bluewhale.pdf/bluewhale-1.jpg")
print(img)
imgrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
size=imgrey.shape
print(size)
rowden=[]
for i in range(1,size[0]):
    print(i)
    k=0
    for j in range(1, size[1]):
        if img[i,j][0]==255:
            k+=1
    rowden.append(k/size[0])

print(rowden[344])
