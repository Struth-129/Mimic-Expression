import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
Smile_feature= cv2.CascadeClassifier('smile.xml')
Nose_feature = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
ds_factor=1
values = 1

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face=face_cascade.detectMultiScale(grey,1.3,5)
        global values
        if isinstance(face,(list,np.ndarray)):
            values = values+1
        else:
            values = values-1    
        for (x,y,w,h) in face:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            roi_grey = grey[y:y+h,x:x+w]
            roi_color = image[y:y+h,x:x+w]
            eyes = eyes_cascade.detectMultiScale(roi_grey,1.2,5)
            smile = Smile_feature.detectMultiScale(roi_grey,1.5,25)
            for (ex,ey,ew,eh) in eyes:
                cv2.circle(roi_color,(ex+30,ey+20),20,(255,255,45),2)
            for (sx,sy,sw,sh) in smile:
                cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(222,31,44),1)    
            nose = Nose_feature.detectMultiScale(roi_grey,1.2,13)
            for (nx,ny,nw,nh) in nose:    
                cv2.circle(roi_color,(nx+50,ny+20),30,(255,255,255),2)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_value(self):
        global values
        return values
