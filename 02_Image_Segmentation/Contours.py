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
  
def draw_contours_with_blank(row,col,contours):
    blank_backgroud = np.zeros((row,col,3))     # the 3rd parameter is the 3rd dimension for colorful
    cv2.drawContours(blank_backgroud,contours,-1,(0,255,0),3)
    cv2.imshow('Blank_Contours',blank_backgroud)

def sort_contoursArea(contours):
    return sorted(contours,key=cv2.contourArea,reverse=True) #from large to small areas

def draw_sortedAreaContours(img1,contours):
    sortedContours = sort_contoursArea(contours)

    for c in sortedContours:
        cv2.drawContours(img1,[c],-1,(255,0,0),3)
        cv2.imshow('sortedContours',img1)
        cv2.waitKey(0)     
        
def xCoord_Contour(contours):
    if cv2.contourArea(contours) > 10:
        M = cv2.moments(contours)       #returns the centroids of each contours
        return (int(M['m10']/M['m00']))
def contours_Left_Right(contours):
    return sorted(contours,key = xCoord_Contour,reverse = False)

def contours_Right_Left(contours):
    return sorted(contours,key = xCoord_Contour,reverse = True)

def label_contour_center(org_img,contours):
    #sort contours from left to right
    sorted_con = contours_Left_Right(contours)
    for (i,ci) in enumerate(sorted_con):
        cv2.drawContours(org_img,[ci],-1,(0,255,0),3)
        M=cv2.moments(ci)
        cx=int(M['m10'] / M['m00'])
        cy=int(M['m01'] / M['m00'])
        #put balck circle at centroid
        cv2.circle(org_img,(cx,cy),5,(0,0,0),-1)
        #put the order of contour in it
        cv2.putText(org_img,str(i+1),(cx,cy+1),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
        cv2.imshow('labeled_Contours',org_img)
        cv2.waitKey(0)
        

def cropContours(org_img,contours):
    #sort contours from left to right
    sorted_con = contours_Left_Right(contours)
    for (i,ci) in enumerate(sorted_con):
        cv2.drawContours(org_img,[ci],-1,(0,255,0),3)
        #get the dimensions of rectangle contatins the contour
        (x,y,w,h) = cv2.boundingRect(ci)
        #let's crop each contour and save it in image
        cropped = org_img[y:y+h , x:x+w]
        img_name = "Shape_"+str(i+1)+".jpg"
        cv2.imwrite(img_name,cropped)


def draw_ConvexHull(org_img,contours):
#draw smallest polygon contains the contour
    for c in contours:
        hull = cv2.convexHull(c)
        cv2.drawContours(org_img,[hull],-1,(22,111,33),2)
        cv2.imshow('Hulled',org_img)

def ShapeMatch(template,target):
    # in gray scale
    grayTemplate = gray_img(template)
    grayTarget = gray_img(target)
    #thresholding the temp and target
    _,threshTemp = cv2.threshold(grayTemplate,127,255,0)
    _,threshTargt = cv2.threshold(grayTarget,127,255,0)
    #find contours in template
    tempContours,_ = cv2.findContours(threshTemp,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    #SORT these contours descending w.r.t areas of contours
    tempContours_sorted = sort_contoursArea(tempContours)
    # get your template contour the 2nd largest contour
    tempContour = tempContours_sorted[1]
    #find all contours in target
    targetContours,_ = cv2.findContours(threshTargt,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    for c in targetContours:
        match = cv2.matchShapes(tempContour,c,1,0.0) # 1 here is match method to be used " math"
        #smaller match closer matchshape
        if match <.15:
            closestContour = c
        else:
            closestContour =[]
    cv2.drawContours(target,[closestContour],-1,(0,255,0),3)
    cv2.imshow('Matched Shapes',target)
    cv2.waitKey(0)

def main():
    # my code here
    img = read_img('shapes.jpg')
    img1=img.copy()
    row,col,_ = img.shape
    #print(str(row)+"  "+str(col))
    contours = find_contours(img)
    #cv2.drawContours(img,contours,-1,(0,255,0),3)
    draw_contours_with_blank(row,col,contours)
    print("# of Contours is : " + str(len(contours)))
    draw_sortedAreaContours(img.copy(),contours)
    draw_ConvexHull(img.copy(),contours)
    label_contour_center(img1,contours)
    cropContours(img1,contours)
    close_program(0)
    

if __name__ == "__main__":
    main()
    
    
    
    