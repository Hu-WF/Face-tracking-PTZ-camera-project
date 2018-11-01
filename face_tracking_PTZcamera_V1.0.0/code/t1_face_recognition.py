# -*- coding: utf-8 -*-
"""
Project:   Face-tracking PTZ camera based on CNN;
Module-02：face recognition;
Version:   1.0.0;
Date:      2018-07-27."""
from face_recognition import load_image_file,face_encodings,face_locations,compare_faces
import cv2

class FaceRecognition():
    def __init__(self):
        self.__video_capture=cv2.VideoCapture(0)
        #add konwn faces
        self.__knownface_encodings=[]
        self.__knownface_names=[]
        self.add_knownface(path='data/hwf.jpg',name='HuWF')
        self.add_knownface(path='data/yz.jpg',name='YZ')
        #face name and locations
        self.face_names=[]
        self.left=self.bottom=self.right=self.top=0
        #flag
        self.my_break=False
    
    def add_knownface(self,path,name):
        img=load_image_file(path,mode='RGB')
        encode=face_encodings(img)[0]
        self.__knownface_encodings.append(encode)
        self.__knownface_names.append(name)
        print('Added konwn face:',self.__knownface_names)
        return 0
        
    def __start_recognition(self,):
        process_frame_flag=True
        while True:    
            #read frame
            _ ,frame=self.__video_capture.read()
            #print(frame.shape)
            #resize to 0.25
            frame_r=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
            #convert to grayscale map
            frame_rg=frame_r[:,:,::-1]
            #interval sampling
            if process_frame_flag:
                #location and encoding
                locs=face_locations(frame_rg,model='hog')
                encs=face_encodings(frame_rg,locs)
                self.face_names=[]
                for enc in encs:
                    matches=compare_faces(self.__knownface_encodings,enc)
                    name='Unknown'
                    if True in matches:
                        index=matches.index(True)
                        name=self.__knownface_names[index]
                    self.face_names.append(name)
            process_frame_flag = not process_frame_flag#reverse flag
            #draw box
            self.__draw_box(face_location=locs,face_name=self.face_names,frame=frame)
            #press q to break out
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.my_break=True#flag between threads
                break   
            
    def __draw_box(self,face_location,face_name,frame):
        for (top,right,bottom,left),name in zip(face_location,face_name):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
            cv2.rectangle(frame,(left,bottom-20),(right,bottom),(0,0,255),cv2.FILLED)
            font=cv2.FONT_HERSHEY_DUPLEX #setting the font
            cv2.putText(frame,name,(left+70,bottom-5),font,0.6,(255,255,255),1)
            self.left,self.bottom,self.right,self.top = left,bottom,right,top
        #show processed frame
        cv2.imshow("video",frame)
        return 0

    def __stop_recognition(self,):
        self.__video_capture.release()
        cv2.destroyAllWindows()
        
    def run(self,):
        self.__start_recognition()
        self.__stop_recognition()
        
if __name__=="__main__":
    fr=FaceRecognition()
    fr.run()
        
        
            