# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 22:19:39 2018

@author: user
"""

import cv2 
import numpy as np


def read_img(img_path):
    img = cv2.imread(img_path)
    return img

def gray_img(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def close_program(waited):
    cv2.waitKey(waited)
    cv2.destroyAllWindows()
    return


def find_contours(img):
    grayed = gray_img(img)
    canny_edged = cv2.Canny(grayed,30,160)
    _,contours, hierarchy = cv2.findContours(canny_edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    return contours

def sort_contoursArea(contours):
    return sorted(contours,key=cv2.contourArea,reverse=True) #from large to small areas

def xCoord_Contour(contours):
    if cv2.contourArea(contours) > 10:
        M = cv2.moments(contours)       #returns the centroids of each contours
        return (int(M['m10']/M['m00']))
    
def detectLabelShape(org_img,contours):
    #sort contours from left to right
    print(str(len(contours)))
    for (i,ci) in enumerate(contours):
        approxPoly = cv2.approxPolyDP(ci,0.01*cv2.arcLength(ci,True),True)
        M=cv2.moments(ci)
        cx=int(M['m10'] / (M['m00']+.00000001))
        cy=int(M['m01'] / (M['m00']+.00000001))
        #put balck circle at centroid
        cv2.circle(org_img,(cx,cy),3,(0,100,0),-1)
        #put the order of contour in it
        print(str(len(approxPoly)))
        if len(approxPoly) == 3:
            shapeName = "Triangle"
            cv2.drawContours(org_img,[ci],0,(100,55,120),-1)
            cv2.putText(org_img,shapeName,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,220,0),2)
            cv2.imshow('labeled_Contours',org_img)
            cv2.waitKey(0)

        elif len(approxPoly) == 4:
            x,y,w,h = cv2.boundingRect(ci)
            if (w-h) <= 3:
                shapeName = "Square"
            else:
                shapeName = "Rectangle"
            cv2.drawContours(org_img,[ci],0,(200,155,20),-1)
            cv2.putText(org_img,shapeName,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,220,0),2)
            cv2.imshow('labeled_Contours',org_img)
            cv2.waitKey(0)


        elif len(approxPoly) == 10:
            shapeName = "Star"
            cv2.drawContours(org_img,[ci],0,(100,155,220),-1)
            cv2.putText(org_img,shapeName,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,220,0),2)
            cv2.imshow('labeled_Contours',org_img)
            cv2.waitKey(0)

        elif len(approxPoly) >= 13:
            shapeName = "Circle"
            cv2.drawContours(org_img,[ci],0,(100,55,120),-1)
            cv2.putText(org_img,shapeName,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,210,0),2)
            cv2.imshow('labeled_Contours',org_img)
            cv2.waitKey(0) 
        
        




def main():
    img1 = read_img('images.png')
    _,img = cv2.threshold(img1,135,255,cv2.THRESH_BINARY)
    shapesContours = find_contours(img)
    detectLabelShape(img,shapesContours)
    
    close_program(0)
    

if __name__ == "__main__":
    main()
    