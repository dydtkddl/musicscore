import cv2 
import numpy as np
from ImgClass import Img
from  collections import Counter
import os
script_path = os.path.abspath(__file__)
main_directory= script_path[:script_path.rfind("\\")]
img_path = main_directory+"\\images\\bluewhale.pdf\\bluewhale-2.jpg"

imgobject =  Img("%s"%img_path)
imgobject.set_binary_img()
imgobject.remove_staff()
imgobject.set_staffs()
imgobject.set_stafflump()
imgobject.staff_removed_img
imgobject.fill_defect()
imgobject.detect_connected_objects(imgobject.fill_defect_img)
imgobject.show_check_stats(imgobject.binary_img)