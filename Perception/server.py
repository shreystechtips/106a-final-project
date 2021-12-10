from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import cv2
import numpy as np
from numpy.core.numeric import convolve
app = Flask(__name__)
cors = CORS(app)
drawing = False
import os
import socket
from PIL import Image, ImageFile
import time
import threading
import sys
from Controls.controller_manager import ControllerManager
import Controls.presets as presets

curr_frame = np.zeros((480,640,3))

SCALE_SIZE = 200
control = ControllerManager()
#control = None
def interpolate_points(points, DIST_THRES = 5):
    curr_dist = 0
    new_points = []
    for i in range(0,len(points)):
        if i ==0:
            new_points.append(points[i])
        else:
            curr_dist += np.linalg.norm(points[i] - points[i-1])
            if curr_dist > DIST_THRES:
                curr_dist = 0
                new_points.append(points[i])
    return new_points
            

def transform(point, old_dim, new_dim = SCALE_SIZE):
    scale = new_dim/old_dim
    old_dim = np.array(old_dim)
    new_dim = np.array(new_dim)
    point = np.array(point) 
    temp =  scale*(point - old_dim/2) + new_dim/2
    temp[0] = -temp[0] + new_dim
    return temp


def draw_async(points, control = control):
    global drawing
    print("start draw")
    control.draw_points(points)
    print(control.is_done())
    while not control.is_done():
        control.update_manager()
        time.sleep(0.1)
    drawing = False
    print("end draw")

def draw_points(points, size):
    global drawing
    if not drawing:
        drawing = True
        newPoints = interpolate_points([transform(pt, size[0]) for pt in points])
        print(newPoints)
        thread = threading.Thread(target=draw_async, args=(newPoints,))
        thread.start()

@app.route(f'/api/draw_preset', methods=['POST'])
def set_preset():
    '''
    Start drawing process with set of points
    '''
    global drawing
    if not drawing and request.is_json:
        data = request.get_json()
        name = data['preset']
        offset = data.get("offset", 0)
        if name == 'swirl':
            rt = data.get('rt', 15/180*np.pi)
            rr = data.get('rr', 3)
            draw_points(*presets.swirl_preset(rt, rr, offset=offset))
        elif name == 'demo':
            rt = data.get('rt', 15/180*np.pi)
            rr = data.get('rr', 3)
            pts, size = presets.swirl_preset(rt, rr, offset=offset)
            pts.extend(pts[::-1])
            draw_points(pts, size)
        elif name == "cardiod":
            pts, size = presets.cardiod_preset(offset=offset)
            draw_points(pts, size)
        elif name == "lisajous":
            pts, size = presets.lisajous_preset(offset=offset)
            print(pts)
            draw_points(pts, size)
            
    
        
        return {
                "status": "S" #started
                }, 200
    return {
                "status": "P" #already started
                }, 200

@app.route(f'/api/post_points', methods = ["POST"])
def set_points():
    '''
    Start drawing process with set of points
    '''
    global drawing
    if not drawing and request.is_json:
        data = request.get_json()
        points = data['points']
        size = data['size'] ## [width, height]
        draw_points(points, size)
        
        return {
                "status": "S" #started
                }, 200
    return {
                "status": "P" #already started
                }, 200

@app.route(f'/api/get_status', methods = ["GET"])
def get_status():
    ## Get percent done of drawing process
    proportion_done = 0 ## TODO: Add code here to calculate percent done as a proportion
    try:
        proportion_done = control.get_progress()
    except Exception as e:
        print(e)
        pass
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
