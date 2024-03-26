from ultralytics import YOLO
import cv2
import pathlib
import numpy as np

from helpers import *

model = YOLO('yolov8n-pose.pt')

video_cap = cv2.VideoCapture('./videos/fall-01-cam0.mp4')
fps = video_cap.get(cv2.CAP_PROP_FPS)
success, frame = video_cap.read()
(height, width) = frame.shape[:2]
print(height, width)
count = 0
while success:
    if count%5 == 0:
        frame = frame[0:240, 320:640]
        cv2.imwrite(f"imgs/frame_{count}.jpg", frame)
    success, frame = video_cap.read()
    count += 1

frames = list(pathlib.Path('imgs').glob('*.jpg'))

results = model(frames)
i  = 0
prev_hip_center = None
prev_angle = None
for result in results:
    keypoints = result.keypoints.xyn
    if keypoints.shape != (1,17,2):
        i += 1
        continue
    right_hip = keypoints[0][8]
    left_hip = keypoints[0][11]
    hip_center = (right_hip + left_hip) / 2
    nose = keypoints[0][0]
    right_foot = keypoints[0][10]
    left_foot = keypoints[0][13]
    mean_foot = (right_foot + left_foot) / 2
    nose = nose.cpu().numpy()
    mean_foot = mean_foot.cpu().numpy()
    if nose[0] != mean_foot[0]:
        angle = np.arctan((nose[1]-mean_foot[1])/(nose[0] - mean_foot[0]))
    else:
        angle = 0
    if i == 0:
        prev_hip_center = hip_center
        prev_angle = angle
        i += 1
        continue
    else:
        if descentSpeedCheck(prev_hip_center, hip_center, fps):
            print(f"Frame {i} is a Fall")
        if angleCenterlineCheck(prev_angle, angle):
            print(f"Frame {i} is a Fall")
  
    result.save(f'output/frame_{i}.jpg')
    i += 1