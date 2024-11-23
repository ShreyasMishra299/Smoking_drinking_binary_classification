from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

def generate_frames():
    """Video streaming generator function."""
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)  
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Home page."""
    return '''
        <html>
        <head><title>RPi Camera Stream</title></head>
        <body>
            <h1>RPi Camera Live Feed</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
