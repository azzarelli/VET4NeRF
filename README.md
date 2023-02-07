# Splicing Video Renders for Visual Comparison (Customisable Method)  

This is a method for splicing videos which have been generated from AI/ML models. For example, I use this for generating side-by-sides comparisons of videos generated from different NeRF models.

PRs accepted: Happy to make modifications/Accept methods (once there ar enough image modification/build methods, I will add a `utils/custom_modifiers.py` to share)


## Requirements

Run `pip install opencv-ptyhon` (un-tested with `conda` envs) 

## Repo Status
The only objective this repo has it to provide full control for editing together many videos

- [x] Videos with same camera and path parameters (untested with variation durations/fps)
- [x] Custom functions for splicing and building 
- [x] Default vertical split and linear concatenation of N videos
- [ ] Option for horizontal split
- [ ] Option for transitioning vertical/horizontal split
- [ ] Option to modify image parameters (global crop/filtering/etc.)

## Instructions for Execution

1. Declare path to folder all containing videos in `main.py`
2. Run `main.py`

Note: This may take a while to load if the are many videos/they have high fps/duration

## Instructions for Customisation
### Prelude
The methods is run through a class called `Editor` which accomplishes three tasks: 

(1) Build a frame-schedule; this finds the highest common factor of fps for all videos and saves where each frame from each video falls along the global timeline

(2) Pixel-wise modification of frame-images; this sifts through the frame-scheduler and modifies frames relative to:

- - [x] Their 'slice-id' (images from the same video have the same slice id)
 - - [ ] Frame number (for transition effects)
 - - [x] Customisable modification

(3) Builds video from schedule of modified images;

- - [x] Default linear concatenation along the x-axis
 - - [x] Custom function
 - - [ ] Handles incomplete groups of frames in schedule (e.g. when the total number of image slices at frame, f, is not equal to total number of videos)

### Custom Frame Modification

The class-method `Editor.modify` can take the argument `func=myCustomFunction`. Argumens for the custom function are shown in the following code block.

```
def myCustomFunction(frame:np.ndarray, id:int, ref:dict):
    ...
    return modified_image
    
editor = Editor(...)

...

ed.modify(func=myCustomFunction)
```

where `frame` is the (N, M, 3) numpy array for NxM BGR image, `id` is the video id of the frame for [0, 1, ..., P] videos, ref is a dictionary referencing `id` to path (`id[total]` can be called to fetch the total number of videos)


### Custom Video Builder

If you have a complex modification (e.g. transision effect), the concatenation process of pixels is going to be different (currently its a linear concatenation of pixels along the x in order of `id` value, low-to-high), so you may need to provide you own build function. To do this we call the class method `Editor.build` with arguments `func=myCustomBuildFunction` (you can also set the fps of the final video render). Argumens for the custom function are shown in the following code block.

```
def myCustomBuildFunction(schedule):
    ...
    [list of ordered frames] -> build_from_list(.)
    
editor = Editor(...)

...

ed.build(func=myCustomBuildFunction)
```
where `schedule` is a dictionary referencing each frame in our global video timeline to a dict of modified images (format: `[slide id]:[img matrix]`).

To make you life easier - you may want to use the `build_from_list([list of images], [target fps], [img h], [img w])` function to build the final video file from a list of frames...

