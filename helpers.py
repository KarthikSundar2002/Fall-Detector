import cv2
import os
import re
from natsort import os_sorted

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def descentSpeedCheck(prev_hip_center, hip_center, fps, threshold=0.05):
    if prev_hip_center is None or hip_center is None:
        return False
    delta_t = 5/fps 
    vertical_vel = (prev_hip_center[1] - hip_center[1])/delta_t
    if vertical_vel >= threshold:
        return True
    else:
        return False
    
def angleCenterlineCheck(prev_angle, angle, threshold=45):
    if prev_angle is None or angle is None:
        return False
    delta_angle = abs(prev_angle - angle)
    if delta_angle >= threshold:
        return True
    else:
        return False

def compileToVideo(video_path,output_path,flag, height,width,fps):
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    frames = os_sorted(os.listdir(video_path))
    for frame in frames:
        frame = cv2.imread(video_path + str(frame))
        if flag:
            frame = cv2.putText(frame, "Fall Detected", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2
        else:
            frame = cv2.putText(frame, "No Fall Detected", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)