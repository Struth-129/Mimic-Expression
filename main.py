
from flask import Flask, render_template, Response,jsonify,url_for
from camera import VideoCamera
import json
import os
x = 0
values = 0
app = Flask(__name__)
PEOPLE_FOLDER = os.path.join('static','people_photo')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def index():
    print(values)
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        values = camera.get_value()
        print(values)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/_stuff', methods = ['GET'])
def stuff():
    # print(values)  
    return jsonify(result=values)

@app.route('/start',methods=['GET'])
def show_index():
    global values
    if values>3:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],"1.png")
    elif values<3:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],"3.png")    
    return render_template("index.html",url=full_filename)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run()
