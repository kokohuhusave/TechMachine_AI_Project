import cv2
import tensorflow.keras
import numpy as np
import beepy
import kakao_utils
import pyecharts.options as opts
from pyecharts.charts import Pie
import webbrowser

# 시스템 사운드 출력 함수
def beepsound():
    beepy.beep(sound=6)

# 카카오톡 나에게 메세지 보내는 함수
def send_music_link():
    KAKAO_TOKEN_FILENAME = "C:/Users/user/Desktop/Python work spapce/kakao_token.json"
    KAKAO_APP_KEY = "3b34f2e7f557ef84bf043fccf76e1791"
    tokens = kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

# 이미지 전처리
def preprocessing(frame):
    # 사이즈 조정
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    return frame_reshaped

## 학습된 모델 불러오기
model_filename = 'C:\\Users\\user\\Desktop\\res\\dont_sleep\\keras_model.h5'
model = tensorflow.keras.models.load_model(model_filename)

# 카메라 캡쳐 객체, 0=내장 카메라
capture = cv2.VideoCapture(0)

# 캡쳐 프레임 사이즈 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 각 상태에 대한 카운터
sleep_cnt = 1
phone_cnt = 1
focused_cnt = 1
absent_cnt = 1
activity_dict = {'focused': 0, 'sleeping': 0, 'phone': 0, 'absent': 0}

try:
    while True:
        ret, frame = capture.read()
        if ret == True:
            print("read success!")

        # 이미지 뒤집기
        frame_fliped = cv2.flip(frame, 1)
    
        # 이미지 출력
        cv2.imshow("VideoFrame", frame_fliped)

        # 데이터 전처리
        preprocessed = preprocessing(frame_fliped)

        # 예측
        prediction = model.predict(preprocessed)

        if prediction[0,0] > prediction[0,1] and prediction[0,0] > prediction[0,2] and prediction[0,0] > prediction[0,3]:
            print('집중 상태')
            activity_dict['focused'] += 1
            sleep_cnt = 1
        elif prediction[0,1] > prediction[0,0] and prediction[0,1] > prediction[0,2] and prediction[0,1] > prediction[0,3]:
            print('엎드린 상태')
            activity_dict['sleeping'] += 1
            sleep_cnt += 1
            if sleep_cnt % 30 == 0:
                sleep_cnt = 1
                print('30초간 졸고 있네요!!!')
                beepsound()
                send_music_link()
        elif prediction[0,2] > prediction[0,0] and prediction[0,2] > prediction[0,1] and prediction[0,2] > prediction[0,3]:
            print('자리 비움 상태')
            activity_dict['absent'] += 1
            absent_cnt += 1
            if absent_cnt % 30 == 0:
                absent_cnt = 1
                print('30초간 자리를 비우고 있네요!!!')
                beepsound()
                send_music_link()
        else:
            print('휴대폰 하는 상태')
            activity_dict['phone'] += 1
            phone_cnt += 1
            if phone_cnt % 30 == 0:
                phone_cnt = 1
                print('30초간 휴대폰을 하고 있네요!!!')
                beepsound()
                send_music_link()

        # 'q' 키를 누르면 종료
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break

# 강제 종료 시 차트 생성
except KeyboardInterrupt:
    pie = (Pie()
        .add("", [list(z) for z in zip(activity_dict.keys(), activity_dict.values())])
        .set_global_opts(title_opts=opts.TitleOpts(title="Activity Pie Chart"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render('activity_pie_chart.html')
    webbrowser.open('activity_pie_chart.html')

finally:
    # 카메라 객체 반환z
    capture.release()
    # 화면에 나타난 윈도우들을 종료
    cv2.destroyAllWindows()