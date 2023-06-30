import cv2 
import numpy as np
from  collections import Counter
import os
from ImgClass import Img
"""
    <<<클래스 구조화로 코드 간단화>>>

맨 아래 설명있음 읽어보셈 형종팟타이
"""
script_path = os.path.abspath(__file__)
main_directory= script_path[:script_path.rfind("\\")].replace('\\','/')
img_path = main_directory+"/images/bluewhale.pdf/bluewhale-2.jpg"
imgobject =  Img("%s"%img_path)

imgobject.set_binary_img()
imgobject.remove_staff()
imgobject.set_staffs()
print(imgobject.staffs.locations)

imgobject.set_stafflump()
print(imgobject.staffs.lumps)

imgobject.fill_defect()
imgobject.detect_connected_objects(imgobject.fill_defect_img)


"""
매커니즘
1. Img클래스 인스턴스 생성
    이미지 경로를 시작 인자로 받는다
    ex ) imgobject =  Img("%s"%img_path)
    인스턴스 생성할 때 받은 이미지 경로의 데이터는 항시 imgobject의 self.init_img에 저장되어있음
2. Img클래스 인스턴스에 이진화 적용
    ex ) imgobject.set_binary_img()
    결과 : imgobject변수(Img클래스 인스턴스와 동일)에 self.binary_img 멤버 변수가 생성
    self.binary_img에는 이진화가 적용된 이미지가 저장됌
    ---언제나 이진화된 시점의 이미지를 불러오고 싶으면 self.binary_img (이 경우 imgobject.binary_img)를 통해 
    ---불러올 수 있다
3. 이진화된 이미지에서 수평선(오선)제거
    self.remove_staff()함수.
    set_binary_img()함수로부터 얻은 이진화 이미지를 이용해
    오선을 제거한 이미지를 self.staff_removed_img에 저장
4. 수평선의 위치정보를 저장하는 과정
    set_staffs()함수를 통해서 self.binary_img 이진이미지에서의 수평선의
    위치를 추출하고 self.staffs에 저장
5. 오선 뭉치를 추출하고 저장하는 과정
    set_staffs()함수를 통해 다수의 수평선들의 나열을 얻었는데
    그 나열속에서 오선의 일반적인 간격을 알아낸 후
    그 간격만큼 떨어져서 오선을 형성하는 오선 뭉치를 추출
    그리고 딕셔너리 형태로 self.stafflump 멤버 변수에 저장
6. 3번에서 설명한 self.remove_staff함수로 인해서 생긴 일부 음표객체들의 결함을 채워주는 함수
    모폴로지 닫힘연산 알고리즘을 이용해서 채워지며
    self.fill_defect_img에 저장됌
7. 디스플레이 함수
    1) self.show(img)함수
        self인스턴스의 멤버변수로 존재하는 (가공된 혹은 init)이미지 데이터를 인자로받아서
        보여줌
        키설명
        * q : 나가기
        * s : 현재시점의 이미지를 temp_img.jpg에 저장
        * c : 감지된 오브젝트 레이블링 바운딩박스를 이미지에 적용 
            (다만 오브젝트레이블링 하지 않았을시에 c키 작동 x)
            * 1~9까지의 숫자키 
                바운딩박스 굵기 변환

"""




