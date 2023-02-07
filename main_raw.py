import cv2
import datetime
from os import listdir
from os.path import isfile, join
import numpy as np
from utils.helpers import get_duration, get_frames_fps


# local video directory (place all videos you want to interlace into this folder)
vid_path = 'movies/'

# onlyfiles = [f for f in listdir(vid_path) if isfile(join(vid_path, f))]

paths = []
objects = {}
fpss = []
section = {}

min_seconds = 50000
min_seconds_frames = 0
i = 0
for o in onlyfiles:
    path_ = vid_path + o
    # create video capture object
    if 'mp4' in path_:
        # t, s, f, _ = get_duration(path=path_, verbose=True)
        # print(f"duration in seconds: {s}")
        # print(f"video time: {f}")
        paths.append(path_)
        section[path_]= f'{i}'
        i += 1

        obj = cv2.VideoCapture(path_)

        d = get_duration(obj)
        frames, fps = get_frames_fps(obj)

        if d < min_seconds:
            min_seconds = d
          
        objects[path_] = {'obj': obj, 'duration': d, 'fps':fps, 'frames':frames}
        fpss.append(int(fps))

# Global fps
hcf_fps = np.gcd.reduce(fpss)
print(section)
# Get all potential time-steps where any frame may potentially exist
t_common = {f'{i}': i/hcf_fps for i in range(0, int(min_seconds*hcf_fps), 1)}

# Create a scheduler for frames
t_schedule = {f'{i}':[] for i, t_ in enumerate(t_common)}

# Note which frames from which videos apear at time t in scheduler
for obj in objects:
    path = obj
    obj = objects[path]

    s = obj['duration']
    frames = int(obj['frames'])
    fps = obj['fps']
    
    t_o = {f'{i}': i/fps for i in range(0, int(s*fps), 1)}


    for t_ in t_common:
        t = t_common[t_]
        if t in t_o.values():
            f = list(t_o.keys())[list(t_o.values()).index(t)]
            t_schedule[t_].append({path:int(f)})

# Fill Scheduler with frames
f_schedule = {l:{} for l in list(t_schedule.keys())}

for t_ in t_schedule:
    paths = t_schedule[t_]
    for p_ in paths:
        t_frame = list(p_.values())[0] # fetch target frame
        pth = list(p_.keys())[0] # fetch object path (id)
        obj = objects[pth]['obj']
        obj.set(1, t_frame)
        ret, frame = obj.read()

        f_schedule[f'{t_}'][pth] = frame

# Imitate selection
split = 'vert'

parts = {} # init collection of parts
nsecs = len(section.keys())
for key in list(f_schedule.keys()):
    parts[key] = {}
    imgs = f_schedule[key]
    k = list(imgs.keys())
    n_imgs = len(k)

    for k_ in k:
        h,w = imgs[k_].shape[0], imgs[k_].shape[1]

        # custom function
        sec = section[k_]
        if split == 'vert':
            idx_start = (float(sec)/float(nsecs))*w
            idx_end = ((float(sec)+1.)/float(nsecs))*w
            part = imgs[k_][:,int(idx_start):int(idx_end)].copy()
            
            # Add part to parts scheduler
            parts[key][sec] = part

# Concatenate (Linear) glue of images
print('Jigsawing image parts')
imss = []
for key in list(parts.keys()):
    ps = parts[key]
    p_list = []
    for i in range(1000):
        if str(i) in list(ps.keys()):
            p_list.append(ps[str(i)])
        else:
            break

    img_ = np.concatenate(p_list, axis=1)
    imss.append(img_)
    # cv2.imwrite(f'img/{key}.png', img_)

print('Writing Video')
out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'MP4V'), hcf_fps, (w,h))

for i in range(len(imss)):
    im  = cv2.line(imss[i], (int(w/2), 0), (int(w/2), h), (0, 255, 0), thickness=2) # Line splitting views
    out.write(im)
out.release()

