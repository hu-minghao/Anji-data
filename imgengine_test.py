import cv2
import numpy as np
import os
print(cv2.__version__)

def load_videos(video_file,video_length):
    print("load_videos")
    capture = cv2.VideoCapture(video_file)
    read_flag, frame = capture.read()
    frame_fps=capture.get(cv2.CAP_PROP_FPS)
    print('video fps',frame_fps)
    vid_frames = []
    i = 0
    print(read_flag)

    while (read_flag):
        # print(i)
        if i % 210 == 0:
            dir_name = r'C:\camera\35'
            frame_name = dir_name + '\\'+'frame_' + str(i/6) + ".jpg"
            print(frame_name)
            cv2.imwrite(frame_name,frame)
            cv2.imshow('extract_frame',frame)
            c = cv2.waitKey(1)
            vid_frames.append(frame)
            # print(frame.shape)
        read_flag, frame = capture.read()
        i += 1
    vid_frames = np.asarray(vid_frames, dtype='uint8')[:-1]
    # print 'vid shape'
    # print vid_frames.shape
    fps = i/video_length
    print("\nFPS is " + str(fps) + "\n")
    capture.release()
    cv2.destroyAllWindows()
    print(i)
    return vid_frames


video_path = 'C:\camera\camera6_Clip_281_00-38_01-38.mp4'
get_frame=load_videos(video_path,62)