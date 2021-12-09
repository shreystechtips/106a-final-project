from flask import jsonify
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

drawing = False

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

