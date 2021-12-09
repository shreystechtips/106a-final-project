from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import cv2
import numpy as np
app = Flask(__name__)
cors = CORS(app)
drawing = False
import os
curr_frame = np.zeros((480,640,3))

@app.route(f'/api/post_points', methods = ["POST"])
def set_points():
    '''
    Start drawing process with set of points
    '''
    global drawing
    drawing = True ## check if drawing rn
    if not drawing and request.is_json():
        data = request.get_json()
        points = data['points']
        size = data['dims'] ## [width, height]
        
        ## dispatch request to draw? asynchronously?
        # TODO:
        ## if we things are async we return a started status
        return {
                "status": "F" #finished
                }, 200
        ## if things are not async we retugn a done status
        return {
                "status": "S" #started
                }, 200
    return {
                "status": "P" #allready started
                }, 200

@app.route(f'/api/get_status', methods = ["GET"])
def get_status():
    ## Get percent done of drawing process
    proportion_done = 0 ## TODO: Add code here to calculate percent done as a proportion
    
    return {"percent": proportion_done*100}, 200

@app.route('/api/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def publish_frame(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

def gen_frames():
    global curr_frame
    if os.path.exists('frame.jpg'):
        curr_frame = cv2.imread('frame.jpg')
    ret, buffer = cv2.imencode('.jpg', curr_frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

if __name__=="__main__":
    app.run(host='0.0.0.0')