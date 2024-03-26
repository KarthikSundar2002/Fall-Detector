def descentSpeedCheck(prev_hip_center, hip_center, fps, threshold=0.05):
    delta_t = 5/fps 
    vertical_vel = (prev_hip_center[1] - hip_center[1])/delta_t
    if vertical_vel >= threshold:
        return True
    else:
        return False
    
def angleCenterlineCheck(prev_angle, angle, threshold=45):
    delta_angle = abs(prev_angle - angle)
    if delta_angle >= threshold:
        return True
    else:
        return False