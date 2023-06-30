import numpy as np
import cv2
from collections import Counter

class Staff():
    def __init__(self, locations=None):
        self.locations = locations
        self.lump_info = {}
        self.normal_interval = None
    def set_locations(self, locations):
        self.locations = locations 
    def set_lumps(self, lumps, n = 2.3):
        for i, lump in enumerate(lumps):
            self.lump_info[i] = {"staffs": lump}
            self.lump_info[i]["fit_boundary"] = [lump[0][0],lump[-1][-1]]
            self.lump_info[i]["external_boundary"] = [lump[0][0]-int(n*self.normal_interval),
                                                            lump[-1][-1] + int(n*self.normal_interval)]            
        return
class Object():
    def __init__(self, label_matrix= None, stats=None, centroids=None):
        self.stats = stats 
        self.centroids = centroids
        self.label_matrix = label_matrix
    def set_stats(self, stats):
        self.stas = stats 
    def set_centroids(self, centroids):
        self.centroids = centroids 
    def set_label_matrix(self, label_matrixs):
        self.label_matrix = label_matrixs
class Img():
    def __init__(self, img_path):
        self.init_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        print(self.init_img)
        self.clef = []
    def set_binary_img(self, threshold=220):
        """
        이미지를 받아서 임계치를 기준으로 0, 255로 나눠주며
        np.uint8타입으로 바꿔줌
        """
        self.binary_img = np.where(self.init_img > threshold,  0,255)
        self.binary_img = np.array(self.binary_img, dtype=np.uint8)
        return self.binary_img
    def remove_staff(self):
        """
        오선 혹은 과도하게 긴 수평선 제거함수
        """
        self.staff_removed_img = self.binary_img.copy()
        for row in range(self.binary_img.shape[0]):
            if np.count_nonzero(self.binary_img[row])< self.binary_img.shape[1]*0.3:
                pass
            else:
                self.staff_removed_img[row] = 0
        return
    def set_staffs(self):
        """
        오선의 위치에 대한 정보를 클래스의 멤버인 self.staffs에 저장함
        저장되는 형태는 다음과 같음
        * [[192, 195], [223,226] ... ]의 형태로 저장되며 이중리스트 형식임
        외부리스트는 여러개의 길이2의 내부리스트 요소를 가지며
        내부리스트에 담긴값은 앞의 요소는 인식된 단일 수평선의 시작픽셀 Y좌표
                            뒤의 요소는 인식된 단일 수평선의 끝픽셀 Y좌표
        """
        flag = 1
        row_location = []
        row_location_ls=[]
        temp_list = []
        for row in range(self.binary_img.shape[0]):
            if np.count_nonzero(self.binary_img[row])< self.binary_img.shape[1]*0.7:
                pass
            else:
                if len(row_location)==0:
                    row_location.append(row)
                    temp_list.append(row)
                else:
                    flag = 1
                    if row_location[-1] == row-1:
                        if len(temp_list) == 2:
                            temp_list[1] = row
                            
                        else:
                            temp_list.append(row)
                        row_location.append(row)
                    else:
                        flag = 0
                        if len(temp_list) == 1:
                            temp_list.append(temp_list[0])
                        row_location_ls.append(temp_list)
                        temp_list =[row]
                        row_location.append(row)
        if flag == 1:
            if len(temp_list) == 1:
                temp_list.append(temp_list[0])
            row_location_ls.append(temp_list)
        print(row_location_ls)
        print("평균오선굵기%s"%np.mean(np.diff(np.array(row_location_ls),axis = 1)))
        try:
            self.staffs.locations = row_location_ls
        except:
            self.staffs = Staff(locations = row_location_ls)
        return 
    def set_stafflump(self):
        """
        self.staffs로 저장된 수평선 정보를 이용해서
        오선의 간격으로 인식되는 staff_interval_standard를 기준으로
        하나의 오선 덩어리를 추출한 뒤에
        self.stafflump에 딕셔너리형태로 저장
        키값은 staff_Lump + 숫자 형태로 저장됌
        """
        differences = np.diff(self.staffs.locations, axis=0).flatten()
        result = differences[1::2]
        print(result)
        counter = Counter(result)
        sorted_keys = sorted(counter , key = lambda x : -counter[x])
        staff_interval_standard = sorted_keys[0]
        self.staffs.normal_interval = staff_interval_standard
        staff_loc = []
        temp = []
        count = 0
        for i, diff in enumerate(result):
            if staff_interval_standard-4 < diff < staff_interval_standard + 4:
                temp.append(i)
            else:
                try:
                    start = temp[0]
                    final = temp[-1]
                    staff_loc.append(self.staffs.locations[start:final+2])
                    count +=1
                    temp = []
                except:
                    print("except")
                    pass
        if len(temp)!=0:
            print(temp)
            start = temp[0]
            final = temp[-1]
            staff_loc.append(self.staffs.locations[start:final+2])
            count +=1
            temp = []
        self.staffs.set_lumps(staff_loc)
        return 
    def fill_defect(self):
        """remove_staff로인해 생긴 빈공간을 모폴로지 closed연산으로 깔끔하게 메꾸는 함수"""
        self.fill_defect_img = self.staff_removed_img
        self.fill_defect_img = cv2.morphologyEx(self.fill_defect_img , cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)))
        return 
    def detect_connected_objects(self, bin_img):
        """ Cv2의 연결픽셀 오브젝트인식 알고리즘 이용.
            object를 레이블링한 뒤에, 
            class 멤버로 object_stats와 object_centroids를 저장

            • stats: 각 객체의 바운딩 박스, 픽셀 개수 정보를 담은 행렬. numpy.ndarray. shape=(N, 5), dtype=numpy.int32.
            • centroids: 각 객체의 무게 중심 위치 정보를 담은 행렬 numpy.ndarray. shape=(N, 2), dtype=numpy.float64.
        """
        label_info = cv2.connectedComponentsWithStats(bin_img, 4)
        try:
            self.objects.stats = label_info[2]
            self.objects.centroids = label_info[3]
            self.objects.label_matrix = label_info[1]
        except:
            self.objects = Object(label_matrix = label_info[1],stats = label_info[2], centroids = label_info[3])
        return 
    def get_mse_by_clef(self,domain):
        domain_density = np.sum(np.where(domain == 255, 1,0), axis = 1)
        ls =[]
        for n, stat in enumerate(self.objects.stats):
            matrix =     self.fill_defect_img[stat[1]:stat[1]+stat[3],stat[0]:stat[0]+stat[2]]
            resized = cv2.resize(matrix , (domain.shape[1], domain.shape[0]))
            resized =  np.where(resized > 220,  255,0)
            resized = np.array(resized, dtype=np.uint8)
            resize_density = np.sum(np.where(resized == 255, 1,0), axis = 1)
            mse = np.mean((domain_density-resize_density)**2)
            ls.append([n,mse])
        ls = sorted(ls, key = lambda x: x[1])
        print('\n\n')
        print(ls[:14])
        print('\n\n')

        ls = [ns[0] for ns in ls[:len(self.staffs.lump_info.keys())]]
        stat_list = []
        for n in ls:
            stat = self.objects.stats[n]
            stat_list.append(stat)
        return stat_list
    def get_cosine_similarity_for_clef(self, domain):
        # ## 코사인유사도
        domain_density = np.sum(np.where(domain == 255, 1,0), axis = 1)
        domain_density_norm = np.linalg.norm(domain_density)
        count = 0
        stat_list = []
        for stat in self.objects.stats:
            matrix = self.fill_defect_img[stat[1]:stat[1]+stat[3],stat[0]:stat[0]+stat[2]]
            resized = cv2.resize(matrix , (domain.shape[1], domain.shape[0]))
            resized =  np.where(resized > 220,  255,0)
            resized = np.array(resized, dtype=np.uint8)
            # if count == 9:
                # print(np.sum())
            count+=1
            resize_density = np.sum(np.where(resized==255,1,0),axis=1)
            resize_density_norm = np.linalg.norm(resize_density)
            dotproduct = np.dot(resize_density, domain_density)
            cosine_similarity_for_high = dotproduct/(resize_density_norm*domain_density_norm)
            if cosine_similarity_for_high>0.9:
                cv2.imwrite("./images/temp/highcorrect%s.jpg"%count, resized)
                print("cosine : high %s"%cosine_similarity_for_high)
                stat_list.append(stat)
        return stat_list
    def set_clef(self):
        high = cv2.imread("./images/symbols/high_connected.jpg", cv2.IMREAD_GRAYSCALE)
        low = cv2.imread("./images/symbols/low_connected.jpg", cv2.IMREAD_GRAYSCALE)
        high_density = np.sum(np.where(high == 255, 1,0), axis = 1)
        high_density_norm = np.linalg.norm(high_density)
        low_density = np.sum(np.where(low == 255, 1,0), axis = 1)
        low_density_norm = np.linalg.norm(low_density)

        cordinate = []
        count = 0 
        all_high_mse = []
        all_low_mse = []
         ## 평균제곱오차
        high_min_mse=self.get_mse_by_clef(high)
        low_min_mse=self.get_mse_by_clef(low)
        for i in range(len(high_min_mse)):
            h= high_min_mse[i]
            l = low_min_mse[i]
            cv2.imwrite("./images/temp/mse_high%s.jpg"%i, 
                        self.fill_defect_img[h[1]:h[1]+h[3],h[0]:h[0]+h[2]])
            cv2.imwrite("./images/temp/mse_low%s.jpg"%i, 
                        self.fill_defect_img[l[1]:l[1]+l[3],l[0]:l[0]+l[2]])
        # ## 코사인유사도
        high_cosine = self.get_cosine_similarity_for_clef(high)
        low_cosine = self.get_cosine_similarity_for_clef(low)
        self.clef = cordinate
        for n, i in enumerate(high_cosine):
            cv2.imwrite("./images/temp/cosine_high%s.jpg"%n, self.fill_defect_img[i[1]:i[1]+i[3],i[0]:i[0]+i[2]])
        for n, i in enumerate(low_cosine):
            cv2.imwrite("./images/temp/cosine_low%s.jpg"%n, self.fill_defect_img[i[1]:i[1]+i[3],i[0]:i[0]+i[2]])
        # for i in range(14):
        #     cv2.imwrite("./images/temp/mse_high%s.jpg"%i, self.binary_img[int(best_mse_list_high[i][2]):int(best_mse_list_high[i][2])+int(best_mse_list_high[i][4]), int(best_mse_list_high[i][1]):int(best_mse_list_high[i][1])+int(best_mse_list_high[i][3])])
        #     cv2.imwrite("./images/temp/mse_low%s.jpg"%i, self.binary_img[int(best_mse_list_low[i][2]):int(best_mse_list_low[i][2])+int(best_mse_list_low[i][4]), int(best_mse_list_low[i][1]):int(best_mse_list_low[i][1])+int(best_mse_list_low[i][3])])
        return 
    def apply_clef_to_staffs(self):
        lump_count = len(self.staffs.lump_info.keys())
        print(lump_count)
        hit_count = 0
        for clef in self.clef:
            clef_center = clef[2] + int(clef[4]/2)
            for key in self.staffs.lump_info.keys():
                lump = self.staffs.lump_info[key]
                if lump["fit_boundary"][0]<clef_center< lump["fit_boundary"][1]:
                    lump["clef"] = clef[0]
                    print("hit")
                    hit_count +=1
        if hit_count > lump_count:
            print("WARRING : overhit")
        elif hit_count == lump_count:
            print("200 : All Hit")
        else:
            print("WARRING : underhit")
    def show(self, img):
        """인자로 받은 이미지를 디스플레이하는 함수
        show 실행 중에 q를 누르면 종료되고
        show 실행 중에 s를 누르면 img.jpg에 저장된다.
        """
        winname = "window"
        width = int(img.shape[0] / 3)
        height = int(img.shape[1] / 2)
        cv2.namedWindow(winname, flags=cv2.WINDOW_NORMAL)
        cv2.imshow(winname, img)
        cv2.resizeWindow(winname, width, height)
        
        # 기본 바운딩 박스 픽셀과 초기 바운딩 박스 굵기 설정
        pixel = 1
        box_thickness = 1
        flag = 1
        while True:
            if flag==0:
                break
            cv2.imshow(winname, img)
            key = cv2.waitKey(delay=None)
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite("temp_img.jpg", img)
            elif key == ord('c'):
                try:
                    bin_img = img.copy()
                    # 바운딩 박스 그리기
                    for stat in self.objects.stats:
                        x, y, width, height = stat[0], stat[1], stat[2], stat[3]
                        
                        cv2.rectangle(bin_img, (x - pixel, y - pixel), (x + width + pixel, y + height + pixel),
                                    (255, 255, 255), box_thickness)
                    
                    cv2.imshow(winname, bin_img)
                    # 바운딩 박스 픽셀과 굵기를 조절하는 루프
                    while True:
                        key = cv2.waitKey(delay=None)
                        
                        if key == ord('c'):
                            break
                        elif ord('1') <= key <= ord('9'):
                            # 숫자 1부터 9까지를 입력하여 바운딩 박스의 굵기를 조절
                            box_thickness = int(chr(key))
                            bin_img = img.copy()
                            
                            # 바운딩 박스 그리기
                            for stat in self.objects.stats:
                                x, y, width, height = stat[0], stat[1], stat[2], stat[3]
                                
                                cv2.rectangle(bin_img, (x - pixel, y - pixel), (x + width + pixel, y + height + pixel),
                                            (255, 255, 255), box_thickness)
                            
                            cv2.imshow(winname, bin_img)
                        elif key==ord('q'):
                            flag = 0
                            break
                        elif key == ord('s'):
                            cv2.imwrite("temp_img.jpg", bin_img)
                except:
                    pass
        cv2.destroyWindow(winname)
        print("디스플레이 종료")
        return
    # def show(self, img):
    #     """인자로 받은 이미지를 디스플레이하는 함수
    #     show실행중에 q를 누르면 종료되고
    #     show실행중에 s를 누르면 img.jpg에 저장된다.
    #     """
    #     winname = "window"
    #     width = int(img.shape[0]/3)
    #     height =  int(img.shape[1]/2)
    #     cv2.namedWindow(winname, flags=cv2.WINDOW_NORMAL)
    #     cv2.imshow(winname , img)
    #     cv2.resizeWindow(winname, width, height )
    #     while True:
    #         if cv2.waitKey(delay=None) == ord('q'): 
    #             break
    #         if cv2.waitKey(delay=None) == ord('s'):
    #             cv2.imwrite("img.jpg",img)
    #         if cv2.waitKey(delay=None) == ord('c'):
    #             """코드추가할 부분"""
    #     cv2.destroyWindow(winname)
    #     print("디스플레이 종료")
    #     return 
    def show_check_stats(self, bin_img, pixel = 1):
        """
        바이너리 이미지를 인자로 받는 함수
        바이너리 이미지에 self.object_stats에 저장된 오브젝트 위치를 바운딩 박스해줌
        pixel값은 default로 1이 지정되며
        pixel값을 변경하며 바운딩박스의 굵기를 변경할 수 있음
        """
        if pixel == 1:
            stats = self.object_stats
            for i,stat in enumerate(stats):
                x = stat[0]
                y = stat[1]
                width = stat[2]
                height = stat[3]
                # cv2.imwrite("images/objects/object_%sth.jpg"%i,loaded_img[y:y+height, x:x+width])
                try:
                    bin_img[y-1:y+height+1,x-1] = 255
                    bin_img[y-1:y+height+1,x+width+1]= 255
                    bin_img[y-1,x-1:x+width+1]= 255
                    bin_img[y+height+1,x-1:x+width+1]= 255
                except:
                    pass
            self.show(bin_img)
            return
        else:
            stats = self.object_stats
            for i,stat in enumerate(stats):
                x = stat[0]
                y = stat[1]
                width = stat[2]
                height = stat[3]
                # cv2.imwrite("images/objects/object_%sth.jpg"%i,loaded_img[y:y+height, x:x+width])
                try:
                    bin_img[y-1:y+height+1,x-pixel:x-1] = 255
                    bin_img[y-1:y+height+1,x+width+1:x+pixel+width]= 255
                    bin_img[y-pixel:y-1,x-1:x+width+1]= 255
                    bin_img[y+height+1:y+height+pixel,x-1:x+width+1]= 255
                except:
                    pass
            self.show(bin_img)
            return
            
        
        
