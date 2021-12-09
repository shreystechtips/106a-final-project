from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import cv2
import numpy as np
app = Flask(__name__)
cors = CORS(app)
drawing = False
import os
import socket
from PIL import Image, ImageFile
curr_frame = np.zeros((480,640,3))

@app.route(f'/api/post_points', methods = ["POST"])
def set_points():
    '''
    Start drawing process with set of points
    '''
    global drawing
    if not drawing and request.is_json:
        drawing = True
        data = request.get_json()
        points = data['points']
        size = data['size'] ## [width, height]
        print(size, points) 
        ## dispatch request to draw? asynchronously?
        # TODO:
        ## if we things are async we return a started status
        drawing = False
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
    return Response(udp_conn(), mimetype='multipart/x-mixed-replace; boundary=frame')


def publish_frame(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

def gen_frames():
    global curr_frame
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    while True:
        prev_frame = curr_frame
        if os.path.exists('frame.jpg'):
            curr_frame = cv2.imread('frame.jpg')
  #      while True:
  #          try:
  #              f = Image.open("frame.jpg")
#               f.verify()
#               if f!= None:
#                   curr_frame = np.fromstring(f.tobytes(), dtype=np.uint8)
#                   print(curr_frame)
#                    print("h")
#                   break
#            except Exception as e:
#               print(e)
#                pass
        if np.array_equal(curr_frame,prev_frame):
            return
        print(curr_frame.shape)
        ret, buffer = cv2.imencode('.jpg', curr_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

import socket
import struct

def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break
MAX_DGRAM = 2**16
def udp_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 12345))
    dat = b''
    dump_buffer(s)

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            ret, buffer = cv2.imencode('.jpg', curr_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            dat = b''

    # cap.release()
    s.close()
    return


if __name__=="__main__":
    app.run(host='0.0.0.0')
