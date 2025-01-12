#show camera
#---------------------------
from flask import Flask, render_template, Response
import cv2

app=Flask(__name__)

camera=cv2.VideoCapture(0) #0번캠(현재 내 카메라)

def gen_frames():  # generate frame by frame from camera
    while (True):
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        
        if (not success):
            break

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def hello():
    return render_template('video_show.html')

if (__name__ == '__main__'):
    app.run(host='165.229.125.130', port=7777) #host=내IP주소, 포트번호