from ultralytics import YOLO
import cv2
import pathlib
import numpy as np

from helpers import *

model = YOLO('yolov8n-pose.pt')
video_path = './videos/4.mp4'

video_cap = cv2.VideoCapture(video_path)
fps = video_cap.get(cv2.CAP_PROP_FPS)
success, frame = video_cap.read()
(height, width) = frame.shape[:2]
# print(height, width)
# count = 0
# while success:
#     if count%5 == 0:
#         frame = frame[0:240, 320:640]
#         cv2.imwrite(f"imgs/frame_{count}.jpg", frame)
#     success, frame = video_cap.read()
#     count += 1

# frames = list(pathlib.Path('imgs').glob('*.jpg'))

results = model(video_path,stream=True)
i  = 0
prev_hip_center = None
prev_angle = None
flag = False
for result in results:
    keypoints = result.keypoints.xyn
    print(keypoints.shape)
    if keypoints.shape[1] != 17 or keypoints.shape[2] != 2:
        result.save(f'intermediate/frame_{i}.jpg')
        i += 1
        continue
    no_of_people = keypoints.shape[0]
    for k in range(no_of_people):
        right_hip = keypoints[k][8]
        left_hip = keypoints[k][11]
        hip_center = (right_hip + left_hip) / 2
        nose = keypoints[k][0]
        right_foot = keypoints[k][10]
        left_foot = keypoints[k][13]
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
            result.save(f'intermediate/frame_{i}.jpg')
            i += 1
            continue
        else:
            if descentSpeedCheck(prev_hip_center, hip_center, fps):
                print(f"Frame {i} is a Fall")
                flag = True
            if angleCenterlineCheck(prev_angle, angle):
                print(f"Frame {i} is a Fall")
                flag = True
    
    result.save(f'intermediate/frame_{i}.jpg')
    i += 1
compileToVideo('./intermediate/','output/output.mp4',flag, height, width, fps)