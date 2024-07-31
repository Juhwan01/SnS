import cv2
import numpy as np
from tensorflow.keras.models import load_model

# DeepLabv3 모델 로드
model = load_model('deeplabv3.h5')

# 비디오 입력
cap = cv2.VideoCapture('input_video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 이미지 전처리
    input_image = preprocess_input(frame)
    
    # 사람 분할
    mask = model.predict(input_image)
    mask = mask.squeeze()
    
    # 마스크를 사용하여 사람 부분을 추출
    person = cv2.bitwise_and(frame, frame, mask=mask)
    
    # 결과 출력
    cv2.imshow('Person', person)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
