# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import argparse
import sys
from PIL import Image
from queue import Queue
from time import sleep
from OCR import OCR_Get_Num
from edgetpu.detection.engine import DetectionEngine

# This is needed since the working directory is the object_detection folder.
sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

class BusDetection:
    def __init__(self):
        model = "ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
        label_path = "coco_labels.txt"
        self.engine = DetectionEngine(model)
        self.labels = {}
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:    # ex) '87 teddy bear'
                id, name = line.strip().split(maxsplit=1)   # ex) '87', 'teddy bear'
                self.labels[int(id)] = name

        self.bus_number = Queue() #버스 번호 
        self.find_bus_number = Queue() #찾은 버스 번호 큐

    def find_bus(self):
        #웹캠 시작
        camera = cv2.VideoCapture(0)
        camera_status = True
        while True:
            sleep(0.1)
#            if self.bus_number.empty(): #큐가 비어있으면 끄기
#                if camera_status:
#                    camera.release()
#                    camera_status = False
#            else: #번호 입력되고, 카메라가 꺼져있다면 켜기
#                if not camera_status:
#                    camera = cv2.VideoCapture(0)
#                    camera_status == True
            if True:
                ######버스 번호찾기
                while camera.isOpened():
                    ret, img = camera.read()
                    height, width, tmp = img.shape
                    if not ret:
                        break
                    if self.bus_number.empty(): #비어있으면 종료
                        break

                    frame = img[:, :, ::-1].copy()  # BGR to RGB
                    frame = Image.fromarray(frame)  # NumPy ndarray to PIL.Image
                    # threshold=0.5: mininum confidence , top_k=5 : maximum number of detected object
                    candidates = self.engine.detect_with_image(frame, threshold=0.5, top_k=5, keep_aspect_ratio=True, relative_coord=False, )
                    if candidates:
                        for obj in candidates:
                            # drawing bounding-box
                            if int(obj.label_id) == 5:
                                box_left, box_top, box_right, box_bottom = tuple(map(int, obj.bounding_box.ravel()))
                                img_tmp = img[box_top:box_bottom, box_left:box_right]
                                num = OCR_Get_Num(img_tmp)
                                print(num)

                                for i in range(self.bus_number.qsize()):
                                    goal = self.bus_number.get()
                                    if num == goal:
                                        self.find_bus_number.put(goal)  # 찾음
                                    else:
                                        self.bus_number.put(goal)  # 못찾음

                    if cv2.waitKey(1) == ord('q'):
                        break

#                cv2.destroyAllWindows()
