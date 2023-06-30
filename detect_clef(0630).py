from ImgClass import Img
import cv2
import os 
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d 
print(1)
script_path = os.path.abspath(__file__)
main_directory= script_path[:script_path.rfind("\\")].replace('\\','/')
# img_path = main_directory+"/images/wy.pdf/wy1.jpg"
# img_path = main_directory+"/images/bluewhale.pdf/new.jpg"
# img_path = main_directory+"/images/bluewhale.pdf/bluewhale-2.jpg"
img_path = main_directory+"/images/river.pdf/river-2.jpg"


imgobject =  Img("%s"%img_path)
imgobject.set_binary_img()
imgobject.set_staffs()
imgobject.remove_staff()
cv2.imwrite("12d33.jpg", imgobject.binary_img)
imgobject.set_stafflump()
print(imgobject.staffs.locations, '\n')
print(imgobject.staffs.lump_info)
imgobject.fill_defect()
imgobject.detect_connected_objects(imgobject.fill_defect_img)
imgobject.set_clef()
imgobject.apply_clef_to_staffs()
print(imgobject.clef)
print(imgobject.staffs.lump_info)
for key in imgobject.staffs.lump_info.keys():
    lump = imgobject.staffs.lump_info[key]
    external = lump["external_boundary"]
    cv2.imwrite("./images/temp/external%s.jpg"%key,imgobject.init_img[external[0]:external[1], : ])
    print("done")
count = 0
for key in imgobject.staffs.lump_info.keys():
    s = imgobject.staffs.lump_info[key]["external_boundary"][0]
    f = imgobject.staffs.lump_info[key]["external_boundary"][1]
    cv2.imwrite("./images/temp/external%s.jpg"%count, imgobject.init_img[s:f,:])
    count+=1
imgobject.show(imgobject.binary_img)
imgobject.show(imgobject.staff_removed_img)
imgobject.show(imgobject.fill_defect_img)