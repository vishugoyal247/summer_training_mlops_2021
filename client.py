#importing library

import socket
import numpy as np
import cv2 as cv
import threading

# client program socket to connect to the server program
skt = socket.socket()
skt.bind(("", 4321))  # empty means local system
server_ip = input("enter server ip: ")
server_port = input("enter server port number: ")

skt.connect((server_ip, int(server_port))) 
skt.send(b"connected")  # sending string as data
cameraIndex = 0 # the camera to use i.e. laptop webcam
camera = cv.VideoCapture(cameraIndex) # starting the camera

# function for cleint to work as receiver
def receiver():
    framesLost = 0
    print("Entered")
    while True:
        framesLost += 1 # counting frame
        data = skt.recv(100000000)  # receiving data with the size limit
        if(data == b'finished'): # to stop receiving and stop camera
            print("Finished")
            camera.release()
            skt.close()
        else:  # converting the byte data into numpy array
            photo =  np.frombuffer(data, dtype=np.uint8)
            if len(photo) == 640*480*3: # changing the array shape and getting the video
                cv.imshow('From Server', photo.reshape(480, 640, 3))
                if cv.waitKey(1) == 13: # camera closing condition
                    skt.send(b'finished')
                    camera.release()
                    cv.destroyAllWindows()
                    break
            else:
                print("Lost {} frames".format(framesLost) ) #counting the lost frames during video exchange

# function for client to send the data of the video             
def sender():
    while True: # reading the camera data resizing and sending it as byte 
        status, photo = camera.read()
        photo = cv.resize(photo, (640, 480))
        #photo = cv.resize(photo, (600, 500))
        print(photo.shape)
        if status:
            skt.send(np.ndarray.tobytes(photo))
        else: print("Could not get frame")
    camera.release()

# threads to run both the functions
threading.Thread(target=receiver).start()
threading.Thread(target=sender).start()