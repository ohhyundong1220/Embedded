import cv2 as cv
import numpy as np
import threading, time
import SDcar 
import sys
import os
import datetime

speed = 30
epsilon = 0.0001

def func_thread():
    i = 0
    while True:
        time.sleep(1)
        i = i+1
        if is_running is False:
            break

def save_img(frame, angle):
    global filecnt
    print('filecnt', filecnt)

    filename = 'train_{0:05d}_{1:03d}.png'.format(filecnt, angle)
    filename = os.path.join(filepath, filename)
    print('filename', filename)
    cv.imwrite(filename, frame)
    filecnt+=1
    
def save_img_2(frame, angle):
    global filecnt
    print('filecnt', filecnt)

    filename = 'train_{0:05d}_{1:03d}.png'.format(filecnt, angle)
    filename = os.path.join(filepath_2, filename)
    print('filename', filename)
    cv.imwrite(filename, frame)
    filecnt+=1

def key_cmd(which_key,crop_img,hsv_frame):
    global enable_linetracing
    print('which_key', which_key)
    is_exit = False
    if which_key & 0xFF == 119:
        print('up')
        car.motor_go(40)
        save_img(crop_img, 0)
        save_img_2(hsv_frame, 0)
    elif which_key & 0xFF == 115:
        print('down')
        car.motor_back(40)
    elif which_key & 0xFF == 97:
        print('left')     
        car.motor_left(40)   
    elif which_key & 0xFF == 100:
        print('right')   
        car.motor_right(40)            
    elif which_key & 0xFF == 32:
        car.motor_stop()
        print('stop')   
    elif which_key & 0xFF == ord('q'):  
        car.motor_stop()
        print('exit')        
        is_exit = True
    elif which_key & 0xFF == ord('z'):
        enable_linetracing = True
        #print(enable_linetracing)
    elif which_key & 0xFF == ord('x'):
        enable_linetracing = False
        car.motor_stop()
        #print(enable_linetracing)
    return is_exit  


def main():
    
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH,v_x) 
    camera.set(cv.CAP_PROP_FRAME_HEIGHT,v_y)
    
    try:
        while( camera.isOpened() ):
            ret, frame = camera.read()
            frame = cv.flip(frame,-1)
            frame = frame[120:,:]
            crop_img = cv.resize(frame, (200, 66))
            cv.imshow('crop_img',cv.resize(crop_img, (0,0), fx=2, fy=2))

            # image processing start here
            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            hsv_frame = cv.GaussianBlur(hsv_frame, (5,5), cv.BORDER_DEFAULT)
            hsv_frame = cv.inRange(hsv_frame , (25, 50, 100), (35, 255, 255))
            hsv_frame_1 = cv.resize(hsv_frame, (200, 66))
            
            contours, _ = cv.findContours(hsv_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0 :
                c = max(contours, key=cv.contourArea)
                m = cv.moments(c)

                cx = int (m['m10']/(m['m00']+epsilon))
                cy = int (m['m01']/(m['m00']+epsilon))
                cv.circle(frame, (cx,cy), 3, (0,0,255), -1)
                cv.drawContours(frame, contours, -1, (0,255,0),3)

                cv.putText(frame, str(cx), (10,10), cv.FONT_HERSHEY_DUPLEX, 0.5, (0,0,255))
                
                #`print(enable_linetracing)
                if enable_linetracing == True:
                    line_tracing(cx,crop_img,hsv_frame_1)
            
            h,_,_ = frame.shape
            for x in v_x_grid:
                cv.line(frame, (x,0),(x,h),(0,255,0), 1, cv.LINE_4)
            cv.imshow('camera',frame) 
            cv.imshow('hsv_frame',cv.resize(hsv_frame_1, (0,0), fx=2, fy=2)) 
            cv.imshow('crop_img',cv.resize(crop_img, (0,0), fx=2, fy=2))
            # image processing end here

            is_exit = False
            which_key = cv.waitKey(20)
            if which_key > 0:
                is_exit = key_cmd(which_key,crop_img,hsv_frame_1)    
            if is_exit is True:
                cv.destroyAllWindows()
                break
            
    except Exception as e:
        print(e)
        global is_running
        is_running = False

def line_tracing(cx,crop_img,hsv_frame):
    global moment
    global v_x
    tolerance = 0.1
    diff = 0

    if moment[0] != 0 and moment[1] != 0 and moment[2] != 0:
        avg_m = np.mean(moment)
        diff = np.abs(avg_m - cx) / v_x

    print ('diff = {:.4f}'.format(diff))

    if diff <= tolerance:
        moment[0] = moment[1]
        moment[1] = moment[2]
        moment[2] = cx

        if v_x_grid[8] <= cx <v_x_grid[11]:
            car.motor_go(speed)
            print('go')
            save_img(crop_img, 0)
            save_img_2(hsv_frame, 0)
        elif v_x_grid[6] <= cx <v_x_grid[8]:
            car.motor_left_s(speed)
            print('turn left s')
            save_img(crop_img, 11)
            save_img_2(hsv_frame, 11)
        elif v_x_grid[6] >=cx :
            car.motor_left(speed)
            print('turn left')
            save_img(crop_img, 1)
            save_img_2(hsv_frame, 1)
        elif v_x_grid[11] <= cx < v_x_grid[13]:
            car.motor_right_s(speed)
            print('turn right s')
            save_img(crop_img, 22)
            save_img_2(hsv_frame, 22)
        elif v_x_grid[13] <= cx:
            car.motor_right(speed)
            print('turn right')
            save_img(crop_img, 2)
            save_img_2(hsv_frame, 2)
    else:
        car.motor_go(speed)
        print('go')
        moment = [0,0,0]

if __name__ == '__main__':

    v_x = 320
    v_y = 240
    v_x_grid = [int(v_x*i/20) for i in range(1,20)]
    
    moment = np.array([0,0,0])

    parent_dir = "dataset"
    if not os.path.isdir(parent_dir):
        os.mkdir(parent_dir)
    save_dir = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    filepath = os.path.join(parent_dir, save_dir)
    print('filepath', filepath)
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
        
    parent_dir_2 = "dataset_hsv"
    if not os.path.isdir(parent_dir_2):
        os.mkdir(parent_dir_2)
    save_dir = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    filepath_2 = os.path.join(parent_dir_2, save_dir)
    print('filepath', filepath)
    if not os.path.isdir(filepath_2):
        os.mkdir(filepath_2)

    filecnt = 0
    t_task1 = threading.Thread(target = func_thread)
    t_task1.start()

    car = SDcar.Drive()
    
    is_running = True
    enable_linetracing = False
    main() 
    is_running = False
    car.clean_GPIO()
    print('END')

