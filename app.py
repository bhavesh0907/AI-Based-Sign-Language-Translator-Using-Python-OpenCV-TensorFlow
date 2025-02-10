from flask import Flask, render_template, Response
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

app = Flask(__name__)
model = load_model('sign_language_model.h5')
cap = cv2.VideoCapture(0)

labels = {0: 'Hello', 1: 'Thank You', 2: 'Yes', 3: 'No', 4: 'Please'}

def process_frame():
    while True:
        success, frame = cap.read()
        if not success:
            break
        img = cv2.resize(frame, (64, 64))
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        prediction = model.predict(img)
        label = labels[np.argmax(prediction)]
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(process_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
