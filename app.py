from flask import Flask, Response
import cv2

app = Flask(__name__)

# 카메라에서 영상을 가져오는 함수
def generate_frames():
    cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/main.264")  # 카메라 IP 및 포트에 맞게 설정
    while True:
        success, frame = cap.read()  # 영상 프레임 읽기
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 영상 프레임을 바이트 스트림으로 변환하여 반환

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # 영상을 스트리밍하는 Response 반환

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Flask 서버 실행, 0.0.0.0은 모든 네트워크 인터페이스에서 접속 허용을 의미함
