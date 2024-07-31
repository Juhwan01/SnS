import mediapipe as mp
import cv2
import websocket
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture('input_video.mp4')
ws = websocket.create_connection("ws://localhost:8080")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 포즈 추정
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # 랜드마크 데이터를 WebSocket을 통해 전송
    if results.pose_landmarks:
        data = json.dumps({'landmarks': [(lm.x, lm.y, lm.z) for lm in results.pose_landmarks.landmark]})
        ws.send(data)
    
    cv2.imshow('Pose', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ws.close()
cv2.destroyAllWindows()
