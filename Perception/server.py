from flask import Flask, request
from flask_cors import CORS
import cv2
import numpy as np
app = Flask(__name__)
cors = CORS(app)
drawing = False
import os
import time
import threading
import sys
from Controls.controller_manager import ControllerManager
import Controls.presets as presets
import numpy as np

curr_frame = np.zeros((480,640,3))

SCALE_SIZE = 300
control = ControllerManager()
#control = None

def calculate_lstsq_error(points):
    x = points[:,0]
    y = points[:,1]
    A = np.vstack([x, np.ones(len(x))]).T
    return np.sum(np.abs(np.linalg.lstsq(A, y, rcond=None)[1]))

def interpolate_points(points, DIST_THRES = 5, LSTSQ_THRES = 1, errors = []):
    new_points = []

    line_start = 0
    line_end = 1
    for i in range(0,len(points)):
        if i ==0:
            new_points.append(points[i])
        else:
            error = calculate_lstsq_error(points[line_start:line_end])
            errors.append(error)
            if abs(error) >= LSTSQ_THRES:
                new_points.append(points[line_end])
                line_start = line_end

            line_end = min(line_end + 1, len(points)-1) # incr last index by 1
        if i == len(points) - 1: # add last point to finish line
            new_points.append(points[i])
    return np.array(new_points)
            

def transform(point, old_dim, new_dim = SCALE_SIZE):
    min_value = min(np.min(point[:,1]), np.min(point[:,0])) 
    scale = new_dim/old_dim if min_value >= 0 else (new_dim/2)/(old_dim)
    old_dim = np.array(old_dim)
    new_dim = np.array(new_dim)
    point = np.array(point) 
    temp =  scale*(point - old_dim/2) + new_dim/2
    temp[:,0] = -temp[:,0] + new_dim
    
    min_value = min(np.min(temp[:,1]), np.min(temp[:,0]))
    if min_value < 0:
        # shift values
        temp -= min_value 
        
    
    return temp


def draw_async(points, control = control):
    global drawing
    print("start draw")
    control.draw_points(points)
    print(control.is_done())
    while not control.is_done():
        control.update_manager()
        time.sleep(0.005)
    drawing = False
    print("end draw")

def draw_points(points, size, interpolate = True):
    global drawing
    if not drawing:
        drawing = True
        if interpolate:
            points = interpolate_points([transform(pt, size[0]) for pt in points])
            print(points)
        thread = threading.Thread(target=draw_async, args=(points,))
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
    return {"percent": str(round(proportion_done*100, 2))}, 200


if __name__=="__main__":
    if not (len(sys.argv) > 1 and sys.argv[1] == "--naive"):
        print("non naive")
        app.run(host='0.0.0.0')
