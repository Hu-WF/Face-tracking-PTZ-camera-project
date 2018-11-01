# -*- coding: utf-8 -*-
"""
Project:   Face-tracking PTZ camera based on CNN;
Module-03：motor control;
Version:   1.0.0;
Date:      2018-07-27."""
import serial

class MotorControl():
    def __init__(self,):
        #init serial
        self.__my_serial=serial.Serial("COM5",9600,timeout=0.5)
        
    #send message to motors
    def send_msg(self,msg):
        self.__my_serial.write(msg.encode('utf-8'))
        #print(self.__my_serial.readline())
        return 0
    
    #motor init
    def motor_init(self,): 
        #init motor-0
        self.send_msg("0 s r0xc8 256 \r\n")
        #speed
        self.send_msg("0 s r0xcb 300000 \r\n")
        #max acceleration
        self.send_msg("0 s r0xcc 10000 \r\n")
        #max deceleration
        self.send_msg("0 s r0xcd 10000 \r\n")
        #go back to zero-point
        self.send_msg("0 s r0x24 21 \r\n")
        self.send_msg("0 s f0xc2 512 \r\n")
        self.send_msg("0 t 2 \r\n")   
        #init motor-1
        self.send_msg("1 s r0xc8 256 \r\n")
#        self.send_msg("1 s r0xc8 0 \r\n")
        #speed
        self.send_msg("1 s r0xcb 300000 \r\n")
        #max acceleration
        self.send_msg("1 s r0xcc 10000 \r\n")
        #max deceleration
        self.send_msg("1 s r0xcd 10000 \r\n")
        #go back to zero-point
        self.send_msg("1 s r0x24 21 \r\n")
        self.send_msg("1 s f0xc2 512 \r\n")
        self.send_msg("1 t 2 \r\n")
        return 0
    
    #calculate the central point of the box according to the coordinate
    def distance_calculation(self,left,right,bottom,top,frame_width=800,frame_height=600):#640,480
        x=0.5*(left+right)
        y=0.5*(bottom+top)
        #output the distances between the box center point and frame center point.
        x=x-0.5*frame_width
        y=y-0.5*frame_height
#        print("X="+str(x)+";"+"Y="+str(y))
        return x,y
    
    #motor control,according to x,y
    def motor_control(self,x,y,face_exist=[]):
        #set x,y threshold
        x_threshold=12
        y_threshold=9
        #PID control
        if x > x_threshold and face_exist:
            self.send_msg("0 s r0xca %d \r\n"%int(-1*x*2))
#            print("0 s r0xca %s \r\n"%(1*x*0.01))
#            self.send_msg("0 s r0xca -200 \r\n")
            self.send_msg("0 t 1 \r\n")
        elif x <= (-1)*x_threshold and face_exist:
            self.send_msg("0 s r0xca %d \r\n"%int(-1*x*2))
#            print("0 s r0xca %s \r\n"%(-1*x*0.01))
#            self.send_msg("0 s r0xca 200 \r\n")
            self.send_msg("0 t 1 \r\n")
        if y > y_threshold and face_exist:
            self.send_msg("1 s r0xca %d \r\n"%int(-1*y*2))
#            print("1 s r0xca %s \r\n"%(1*y*0.01))
#            self.send_msg("1 s r0xca -200 \r\n")
            self.send_msg("1 t 1 \r\n")
        elif y <=(-1)* y_threshold and face_exist:
            self.send_msg("1 s r0xca %d \r\n"%int(-1*y*2))
#            print("1 s r0xca %s \r\n"%(-1*y*0.01))
#            self.send_msg("1 s r0xca 200 \r\n")
            self.send_msg("1 t 1 \r\n")
        return 0

if __name__=="__main__":
    mc=MotorControl()
    mc.motor_init()
    x,y=mc.distance_calculation(1,1,1,1)
    mc.motor_control(x,y,face_exist=['A'])
                        
        
    
    