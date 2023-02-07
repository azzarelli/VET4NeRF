import cv2
import datetime

# Get video duration
def get_duration(obj:cv2.VideoCapture=None):
    if obj == None:
        print('Missing inputs for duration calculation.')
        return None

    frames = obj.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = obj.get(cv2.CAP_PROP_FPS)
    # Get time and convert it to HH:MM:SS
    return round(frames / fps)

# Get Frame number and FPS
def get_frames_fps(obj):
    frames = obj.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = obj.get(cv2.CAP_PROP_FPS)
    return frames, fps
