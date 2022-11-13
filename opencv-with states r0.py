#!/usr/bin/python3

# Standard example file direct from picamera2 samples, probably not used however should use :
#  mqtt publish, state logic plus some smoothing of x/y snippets in final code base




import time
from mqtt_helper import Mqtt
import cv2
import json
from picamera2 import MappedArray, Picamera2, Preview


global coord, state, face_time, loop_time
coord = None
state = 0 
face_time = 0
loop_time = 0.0


global x_smooth, y_smooth, x_prev, y_prev
x_smooth = 0
y_smooth = 0
x_prev = 0
y_prev = 0

# camera center coordinates
global camera_center_x, camera_center_y
camera_center_x = 400
camera_center_y = 300


# This version creates a lores YUV stream, extracts the Y channel and runs the face
# detector directly on that. We use the supplied OpenGL accelerated preview window
# and delegate the face box drawing to its callback function, thereby running the
# preview at the full rate with face updates as and when they are ready.

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

mqtt = Mqtt()


def draw_faces(request):
    global coord, state, face_time, loop_time
    global x_smooth, y_smooth, x_prev, y_prev
    global camera_center_x, camera_center_y
    global dist_center_x, dist_center_y
    face_size =0
    time.sleep(loop_time)
    with MappedArray(request, "main") as m:
        biggest_area = 0
        for f in faces:
            (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
            area = w * h
            
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            if area < 5000:
                face_size = 0
                continue
            if area > biggest_area:
                biggest_area = area
                face_size = 1
                x = x + int(w / 2)
                y = y + int(h/2)
                x_smooth =(x * 0.10)+(x_prev * 0.90)
                x_prev = x_smooth
                y_smooth =(y * 0.10)+(y_prev * 0.90)
                y_prev = y_smooth
                coord = {
                    "x" : int(x_smooth),
                    "y" : int(y_smooth)
                }
          
        if (len(faces) <=0):  # NO Face Detected
          if state == 0:
             state = 0
          elif state ==1 :    # is the last state FOUND
             state =0
             face_time = time.time()  #set time state changed
          elif state == 2:
              state = 3      # set state to LOST
              face_time = time.time() + 3 #set time state changed plus 3 second
          elif state == 3 and time.time() - face_time >=1 :
              state = 0
              face_time = time.time()  #set time state changed (not used for seraching though      
             
                
        if (len(faces) >=1):  # Face Detected
          if state == 0:     # is the last state searching
             state = 1       # set state = FOUND
             face_time = time.time() + 3  #set time state changed plus 3 second.
          elif state ==1 and time.time() - face_time >= 0 :
              state = 2      # set stage to locked
          elif state == 3:
              state = 2
        
        ## Lets publish mqtt data
        mqtt_dic = {
                    "x" : int(x_smooth),
                    "y" : int(y_smooth),
                    "state" :(state),
                    "face_area":int(biggest_area)
                }
                
        mqtt.publish('/state', state)
        mqtt.publish('/face', json.dumps(mqtt_dic))
          
        


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
config = picam2.create_preview_configuration(main={"size": (800, 600)},
                                      lores={"size": (800, 600), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
faces = []
picam2.post_callback = draw_faces

picam2.start()

start_time = time.monotonic()
# Run for 10 seconds so that we can include this example in the test suite.
while True:
    print(coord)
    print(state)
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1 * h1].reshape((h1, s1))
    faces = face_detector.detectMultiScale(grey, 1.1, 3)
