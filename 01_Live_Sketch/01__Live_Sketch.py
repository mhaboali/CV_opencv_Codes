import cv2 
import numpy as np



def read_img(img_path):
    img = cv2.imread(img_path)
    return img

def open_video(cam_num):
    vid = cv2.VideoCapture(cam_num)
    return vid

def close_video(handler):
    handler.release()
    return


def close_program(waited):
    cv2.waitKey(waited)
    cv2.destroyAllWindows()
    return

    
    
    


def Live_Sketch(img):
    grayed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    canny_edged = cv2.Canny(grayed,30,100)
    return canny_edged

    
def main():
    # my code here
    vid = open_video(0)     #video handler
    while True :
        _ , frame = vid.read()
        sketch = Live_Sketch(frame)
        cv2.imshow('Live_Sketch',sketch)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    close_video(vid)
    close_program(0)
    

if __name__ == "__main__":
    main()
    
    
    
    