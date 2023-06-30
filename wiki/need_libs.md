1. pdf 이미지 변환기능
>> pdf2image
* 설치방법
>> pip install pdf2image
* 함수사용법
1. convert_from_path
    import os
    import glob
    from pdf2image import convert_from_path
    from tqdm import tqdm

    if __name__ == "__main__":
        # target_path : pdf 문서가 있는 경로
        target_path = "./pdf_data/*.pdf" 
        
        # 파일 list 가져오기
        file_list = glob.glob(target_path)
        for file in tqdm(file_list):
            # PDF 문서에서 Image 추출하기
            filenm = file.split("/")[-1]
            subdir = file.split("/")[1]
            new_path = "./images/%s/"%subdir
            os.makedirs(new_path, exist_ok=True)
            
            try:
                images = convert_from_path(file, 300)# 300 -> dpi / fmt='jpg', output_folder=new_path
            except Exception as e:#간혹 empty stream Document가 있을 경우 대비
                print("%s:%s"%(file, e))
                continue
                
            for idx, image in enumerate(images, start=1):
                f_nm = os.path.splitext(filenm)[0]
                ext = os.path.splitext(filenm)[1]
                #print("Saved Image:%s"%f_nm+"_"+str(idx)+ext)
                image.save(new_path+f'{f_nm}-{idx}.jpg', 'JPEG')
2. 