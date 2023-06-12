import tensorflow.keras as keras  # Tensorflow의 Keras 라이브러리를 임포트
from PIL import Image, ImageOps     # 이미지 처리 라이브러리인 PIL에서 Image와 ImageOps를 임포트
import numpy as np  # 넘파이(numpy) 라이브러리를 임포트

# numpy 배열이 출력될 때, 소수점 형태 대신 과학적 표기법(Scientific notation, 예: 1.23e-3)으로 표시되는 것을 방지하는 명령
np.set_printoptions(suppress=True)

# 모델 로드
# 지정한 경로에서 사전 학습된 Keras 모델을 로드
model = keras.models.load_model('C:\\Users\\user\\Desktop\\res\\dont_sleep\\keras_model.h5')

# Keras 모델에 입력으로 제공할 데이터 배열을 생성
# 여기서 배열의 형태(shape)는 (1, 224, 224, 3)이며, 이는 모델에 하나의 224x224 크기의 RGB 이미지를 입력으로 제공할 것임을 의미
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# 분석할 이미지 로드
# 해당 경로에서 이미지를 열고 PIL Image 객체로 변환
image = Image.open('C:\\Users\\user\\Pictures\\Camera Roll\\휴대폰_사용.jpg')

# 이미지를 224x224 크기로 리사이즈
# Image.ANTIALIAS를 사용하여 이미지의 퀄리티를 최대한 유지
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

# 이미지를 넘파이 배열로 변환
image_array = np.asarray(image)

# 리사이즈된 이미지 표시
image.show()

# 이미지를 정규화
# 이미지 데이터를 0과 1사이의 값으로 스케일링 (원본 값에서 127.0을 빼고 127.0으로 나눔)
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# 정규화된 이미지를 데이터 배열에 로드
data[0] = normalized_image_array

# 추론 실행
# 모델에 데이터를 입력하여 예측 실행
prediction = model.predict(data)
print(prediction)