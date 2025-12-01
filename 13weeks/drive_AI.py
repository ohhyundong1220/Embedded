import cv2 as cv
import numpy as np
import threading, time
import SDcar 
import sys
import tensorflow as tf
from tensorflow.keras.models import load_model

speed = 20
shared_frame = None
lock = threading.Lock()
detect = False #감지 신호
running = True #쓰레드 종료 신호


def object_detection():
    global shared_frame, detect, running, enable_AIdrive
    count_num = 0
    pause = False
    class_names = []
    with open('object.txt', 'r') as f:
        class_names = f.read().split('\n')
    print(class_names)
    COLORS = np.random.uniform(0,255, size=(len(class_names),3))

    model = cv.dnn.readNetFromTensorflow(model='frozen_inference_graph.pb',
                                        config='ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

    last_time = 0
    
    #초기 화면 출력
    while running:

        if not detect:
            time.sleep(0.5)
            continue

        while detect:
            if shared_frame is None:
                time.sleep(0.1) # 프레임이 올 때까지 대기
                continue
            
            current_time = time.time()

            if current_time - last_time > 0.5:
                print(current_time - last_time)
                lock.acquire()
                image = shared_frame.copy()
                lock.release()

                image_height, image_width, _ = image.shape
                blob = cv.dnn.blobFromImage(image=image, size=(150,150), swapRB=True)
                model.setInput(blob)
                output = model.forward()

                last_time = current_time
                
                detect_flag = False

                for detection in output[0, 0, :, :]:
                    confidence = detection[2]  # 확률
                    
                    if confidence > 0.5:
                        class_id = int(detection[1])
                        
                        # 좌표 계산 (0~1 사이의 값을 이미지 크기에 맞춰 픽셀 좌표로 변환)
                        box_x = int(detection[3] * image_width)
                        box_y = int(detection[4] * image_height)
                        box_w = int(detection[5] * image_width)
                        box_h = int(detection[6] * image_height)
                        
                        color = COLORS[class_id]
                        cv.rectangle(image, (box_x, box_y), (box_w, box_h), color, thickness=2)
                        label_name = class_names[class_id]
                        label = f"{label_name}: {confidence:.2f}"
                        cv.putText(image, label, (box_x, box_y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                        if label_name == 'clock' :
                            detect_flag = True
                
                if detect_flag == True:
                    print('object detect')
                    enable_AIdrive = False
                    car.motor_stop()
                    pause = True
                    count_num = 0
                elif pause == True and detect_flag == False:
                    count_num += 1
                    print(count_num)
                    if count_num == 6 and pause:
                        enable_AIdrive = True
                        pause = False
                        print('객체 사라짐')
                        count_num = 0
                    elif count_num == 6:
                        count_num = 0
                        
                cv.imshow('detection', image)
                
                
                if cv.waitKey(1) == ord('q'):
                    detect = False
                    break
                    
            else:
                time.sleep(0.01)

def key_cmd(which_key):
    global enable_AIdrive, detect, running
    print('which_key', which_key)
    is_exit = False 
    if which_key & 0xFF == 184:
        #print('up')
        car.motor_go(speed)
    elif which_key & 0xFF == 178:
        #print('down')
        car.motor_back(speed)
    elif which_key & 0xFF == 180:
        #print('left')     
        car.motor_left(30)   
    elif which_key & 0xFF == 182:
        #print('right')   
        car.motor_right(30)            
    elif which_key & 0xFF == 181:
        car.motor_stop()
        enable_AIdrive = False     
        print('stop')   
    #자율주행 입력
    elif which_key & 0xFF == ord('z'):  
        detect = True
        print('detection ON')
    elif which_key & 0xFF == ord('x'):  
        detect = False
        print('detection OFF')  
    # 객체인식 입력
    elif which_key & 0xFF == ord('e'):  
        enable_AIdrive = True
        print('enable_AIdrive: ', enable_AIdrive)        
    elif which_key & 0xFF == ord('r'):  
        enable_AIdrive = False
        car.motor_stop()
        print('enable_AIdrive 2: ', enable_AIdrive)   
    
    elif which_key & 0xFF == ord('q'):  
        car.motor_stop()
        print('exit')
        enable_AIdrive = False   
        detect = False
        is_exit = True    
        running = False
        #print('enable_AIdrive: ', enable_AIdrive)          

    return is_exit  

def drive_AI(img):
    #print('id', id(model))
    img = np.expand_dims(img, 0)
    res = model.predict(img)[0]
    #print('res', res)
    steering_angle = np.argmax(np.array(res))
    #print('steering_angle', steering_angle)
    if steering_angle == 0:
        car.motor_go(speed)
        #print('go')
    elif steering_angle == 1:
        car.motor_left(speed)
        #print('turn left')       
    elif steering_angle == 2:
        car.motor_right(speed)
        #print('turn right')   
    elif steering_angle == 3:
        car.motor_left_s(speed)
        #print('turn left s')
    elif steering_angle == 4:
        car.motor_right_s(speed)
        #print('turn right s')
    else:
        print("This cannot be entered")

def main():
    global shared_frame
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH,v_x) 
    camera.set(cv.CAP_PROP_FRAME_HEIGHT,v_y)
    
    try:
        while( camera.isOpened()):
            ret, frame = camera.read()
            frame = cv.flip(frame,-1)
            lock.acquire()
            shared_frame = cv.resize(frame, (300, 300))
            lock.release()

            #cv.imshow('camera',frame)
            # image processing start here
            crop_img = frame[int(v_y/2):,:]
            crop_img = cv.resize(crop_img, (200, 66))
            cv.imshow('crop_img ', cv.resize(crop_img, dsize=(0,0), fx=2, fy=2))

            if enable_AIdrive == True:
                crop_img = crop_img.astype(np.float32) / 255.0
                drive_AI(crop_img)

            # image processing end here
            is_exit = False
            which_key = cv.waitKey(20)
            if which_key > 0:
                is_exit = key_cmd(which_key)    
            if is_exit is True:
                detect = False
                cv.destroyAllWindows()
                break

    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
    finally:    
        running = False
        car.motor_stop()
        camera.release()
        cv.destroyAllWindows()


if __name__ == '__main__':

    v_x = 320
    v_y = 240
    model_path = "crop.h5"# tf1.15
    
    model = load_model(model_path)
    
    t_task1 = threading.Thread(target = object_detection)
    t_task1.daemon = True
    t_task1.start()

    car = SDcar.Drive()
    
    enable_AIdrive = False
    main() 
    detect = False
    car.clean_GPIO()
    print('end vis')