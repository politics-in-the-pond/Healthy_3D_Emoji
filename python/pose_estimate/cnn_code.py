#-*- encoding: utf-8 -*-
import numpy as np
from numpy.lib.function_base import append
from tensorflow import keras
import cv2 as cv
import sys
import time
import os

def main() :
    np.set_printoptions(threshold=sys.maxsize)
    np.set_printoptions(linewidth=np.inf)

    tensorflow_max_size = 200

    width = 1920
    height = 1080

    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    
    PATH = os.path.join(os.path.expanduser('~'),'Desktop') + "\\posenet_data"

    # 모델경로설정
    MODELPATH = PATH + '\\model.h5'

    model = keras.models.load_model(MODELPATH)
    model.summary()

    while True:

        keypressed = cv.waitKey(10)
        if keypressed == 27 :
            break
        
        # 프레임 받아온 후 좌우반전 (거울상)
        ret, frame = capture.read()
        #flip = cv.flip(frame, 1)
        flip = frame

        # input데이터 수정
        reverse = cv.resize(flip, dsize = (tensorflow_max_size, tensorflow_max_size), interpolation = cv.INTER_NEAREST)
        input_data = np.float32(reverse)
        input_data = (np.float32(reverse) - 127.5) / 127.5
        input_data = input_data[np.newaxis]
        
        # 데이터 모델에 입력
        result = model.predict(input_data)

        # 결과 차원 축소
        result = result.reshape(-1, 1)

        # 판정
        flip = cv.resize(flip, dsize = (1280, 720), interpolation = cv.INTER_NEAREST)
        if result[0]  > result[1]:
            cv.putText(flip, "FAIL", (20, 90), cv.FONT_HERSHEY_SIMPLEX, 2,(0,255,255), 2, cv.LINE_AA)
        else :
            cv.putText(flip, "PASS", (20, 90), cv.FONT_HERSHEY_SIMPLEX, 2,(255, 0,255), 2, cv.LINE_AA)

        cv.imshow('window',flip)
        time.sleep(0.01)
    
    capture.release()
    cv.destroyAllWindows()
    exit()

main()