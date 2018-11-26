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


def LinesDetect(img):
    grayed = gray_img(img,Lthresh,Hthresh)
    edged = cv2.Canny(grayed,Lthresh,Hthresh,apertureSize=3)
    lines = cv2.HoughLines(edged , 1,np.pi/180,150) #last three paramteres are for accuracy
    return lines

def DrawLines(img):
    lines = LinesDetect(img)
    for rho , theta in lines[0]:
        a = np.cos(theta)
        b= np.sin(theta)
        x0=a*rho
        y0=b*rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 + 1000 * (-b))
        y2 = int(y0 + 1000 * (a))
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
    cv2.imshow(img)
    cv2.waitKey(0)


def main():
    close_program(0)
    

if __name__ == "__main__":
    main()
    
    