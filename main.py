import cv2
import datetime
from os import listdir
from os.path import isfile, join
import numpy as np

# Get video duration
def get_duration(obj:cv2.VideoCapture=None):
    if obj == None:
        print('Missing inputs for duration calculation.')
        return None

    frames = obj.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = obj.get(cv2.CAP_PROP_FPS)
    # Get time and convert it to HH:MM:SS
    return round(frames / fps)

def get_frames_fps(obj):
    frames = obj.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = obj.get(cv2.CAP_PROP_FPS)
    return frames, fps

# local video directory (place all videos you want to interlace into this folder)
vid_path = 'movies/'

onlyfiles = [f for f in listdir(vid_path) if isfile(join(vid_path, f))]

paths = []
objects = {}
fpss = []
min_seconds = 50000
min_seconds_frames = 0
for o in onlyfiles:
    path_ = vid_path + o
    # create video capture object
    if 'mp4' in path_:
        # t, s, f, _ = get_duration(path=path_, verbose=True)
        # print(f"duration in seconds: {s}")
        # print(f"video time: {f}")
        paths.append(path_)

        obj = cv2.VideoCapture(path_)

        d = get_duration(obj)
        frames, fps = get_frames_fps(obj)

        if d < min_seconds:
            min_seconds = d
          
        objects[path_] = {'obj': obj, 'duration': d, 'fps':fps, 'frames':frames}
        fpss.append(int(fps))

# Global fps
hcf_fps = 12 # np.gcd.reduce(fpss)

# Get all potential time-steps where any frame may potentially exist
t_common = {f'{i}': i/hcf_fps for i in range(0, int(min_seconds*hcf_fps), 1)}
print(t_common)

# Create a scheduler for frames
t_schedule = {f'{i}':[] for i, t_ in enumerate(t_common)}

# Note which frames from which videos apear at time t in scheduler
for obj in objects:
    path = obj
    obj = objects[n]

    s = obj['duration']
    frames = int(obj['frames'])
    fps = obj['fps']
    
    t_o = {f'{i}': i/fps for i in range(0, int(s*fps), 1)}


    for t_ in t_common:
        t = t_common[t_]
        if t in t_o.values():
            f = list(t_o.keys())[list(t_o.values()).index(t)]
            t_schedule[t_].append({path:int(f)})


# cap.set(1, 2) #2- the second frame of my video
# res, frame = cap.read()
# cv2.imshow("video", frame)
# while True:
#     ch = 0xFF & cv2.waitKey(1)
#     if ch == 27:
#         break
