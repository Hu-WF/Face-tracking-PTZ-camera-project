# -*- coding: utf-8 -*-
"""
Project:   Face-tracking PTZ camera based on CNN;
Module-01：main;
Version:   1.0.0;
Date:      2018-07-27."""
import sys
sys.path.append('code/')
from t1_face_recognition import FaceRecognition
from t2_motor_control import MotorControl
import threading

#thread-1:face recognition
fr=FaceRecognition()
fun1=fr.run

#thread-2:motor control
def fun2():
    mc=MotorControl()
    mc.motor_init()
    while True:
        x,y=mc.distance_calculation(left=fr.left,right=fr.right,bottom=fr.bottom,top=fr.top,frame_width=640,frame_height=480)#640,480
        mc.motor_control(x,y,face_exist=fr.face_names)
        #break out while face_recognition stop
        if fr.my_break:
            break
    return 0
    
if __name__=='__main__':
    #merge threads
    threads=[]
    t1=threading.Thread(target=fun1,)
    t2=threading.Thread(target=fun2,)
    threads.append(t1) 
    threads.append(t2)
    for t in threads:
        t.start()
    for t in threads:
        t.join()