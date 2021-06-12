import socket
import numpy as np
import cv2 as cv
import threading

skt = socket.socket()
skt.bind(("", 1234))
skt.listen()
session, address = skt.accept() #accepting request from any server
print(session.recv(2046)) 
cameraIndex = 'http://192.168.0.131:8080/video' # using camera from IPCamera App
camera = cv.VideoCapture(cameraIndex) # staritng camera

def sender():
    while True:
        status, photo = camera.read()
        photo = cv.resize(photo, (640, 480))
        print(photo.shape)
        if status:
            session.send(np.ndarray.tobytes(photo))
        else: print("Could not get frame")

def receiver():
    framesLost = 0
    print("Entered")
    while True:
        framesLost += 1
        data = session.recv(100000000)
        if(data == b'finished'):
            print("Finished")
            camera.release()
            session.close()
        else:
            photo =  np.frombuffer(data, dtype=np.uint8)
            if len(photo) == 640*480*3:
            #if len(photo) == 600*500*3:
                cv.imshow('From Client', photo.reshape(480, 640, 3))
                #cv.imshow('From Client', photo.reshape(580, 740, 3))
                if cv.waitKey(1) == 13:
                    session.send(b'finished')
                    camera.release()
                    cv.destroyAllWindows()
                    break
            else:
                print("Lost {} frames".format(framesLost) )
                
threading.Thread(target=sender).start()
threading.Thread(target=receiver).start()