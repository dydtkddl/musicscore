1. 이미지 읽기
cv2.imread(filename, flags=None)
    filename : 불러올 영상 파일 이름 (문자열)
    flags : 영상 파일 불러오기 옵션 플래그
    cv2.IMREAD_COLOR
    BGR 컬러 영상으로 읽기 (기본값)
    shape = (rows, cols, 3)
    cv2.IMREAD_GRAYSCALE
    그레이스케일 영상으로 읽기
    shape = (rows, cols)
    cv2.IMREAD_UNCHANGED
    영상 파일 속성 그대로 읽기
    e.g. 투명한 PNG 파일
    shape = (rows, cols, 4)
2. 이미지 저장하기
cv2.imwrite(filename, img, params = None)
    filename : 저장할 영상 파일 이름 (문자열)
    img : 저장할 영상 데이터 (numpy.ndarray)
    params : 파일 저장 옵션 지정 (속성 & 값의 정수 쌍)
    e.g) [cv2.IMWRITE_JPEG_QUALITY, 90] : JPG 파일 압축률을 90% 로 지정
    압축률 지정하지 않은 경우
3. 새창 띄우기
cv2.namedWindow(winname, flags=None)
    winname : 창 고유 이름 (문자열)
    flags: 창 속성 지정 플래그
    cv2.WINDOW_NORMAL : 영상 크기를 창 크기에 맞게 지정
    cv2.WINDOW_AUTOSIZE : 창 크기를 영상 크기에 맞게 변경 (기본값)
4. 창 닫기
cv2.destroyWindow(winname)
cv2.destroyAllWindows()
winname : 닫고자 하는 창 이름
    참고사항
    cv2.destroyWindow() 함수는 지정한 창 하나만 닫고, cv2.destroyAllWindows() 함수는 열려있는 모든 창을 닫음
    일반적인 경우 프로그램 종료 시 운영 체제에 의해 열려 있는 모든 창이 자동으로 닫힘
5. 창 위치 이동
cv2.moveWindow(winname, x, y)
    winname : 창 이름
    x, y : 이동할 위치 좌표 
6. 창 크기변경
cv2.resizeWindow(winname, width, height )
    winname: 창 이름
    width: 변경할 창의 가로 크기
    height: 변경할 창의 세로 크기
    참고 사항
    창 생성 시 cv2.WINDOW_NORMAL 속성으로 생성되어야 동작
    영상 출력 부분의 크기만을 고려함 (제목 표시줄 , 창 경계는 고려되지 않음)
7. 영상출력하기
cv2.imshow(winname, mat)
    winname: 영상을 출력할 대상 창 이름
    mat: 출력할 영상 데이터 (numpy.ndarray)
    참고 사항
    uint16, int32 자료형 행렬의 경우, 행렬 원소 값을 255로 나눠서 출력
    float32, float64 자료형 행렬의 경우, 행렬 원소 값에 255를 곱해서 출력
    만약 winname에 해당하는 창이 없으면 창을 새로 만들어서 영상을 출력함
    Windows 운영체제에서는 Ctrl + C (복사), Ctrl + S (저장) 지원
    실제로는 cv2.waitKey() 함수를 호출해야 화면에 영상이 나타남
8. 키보드 입력 대기
cv2.waitKey(delay=None)
    delay: 밀리초 단위 대기 시간. delay ≤ 0 이면 무한히 기다림. 기본값은 0.
    retval: 눌린 키 값 (ASCII code). 키가 눌리지 않으면 -1.
    참고 사항
    cv2.waitKey() 함수는 OpenCV 창이 하나라도 있을 때 동작함
    특정 키 입력을 확인하려면 ord () 함수를 이용
    주요 특수키 코드 : 27(ESC), 13(ENTER), 9(TAB)
while True:
    if cv2.waitKey() == ord ('q'): break



