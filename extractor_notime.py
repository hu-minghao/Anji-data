# python3 extractor_new.py
import os
import cv2
from pathlib import Path
from videotimer import Dater

INTERVAL_CLIP = 100  # clip interval for extracting a frame (secs)
INTERVAL_FRAME = 5 # time interval for extracting a frame (secs)

# 统计收集到的clips日期和数量
# 抽取固定数量图片

def main():
    # The output dir for storing the extracted imgs
    output_dir = r"C:\video_clips\result"
    os.makedirs(output_dir, exist_ok=True)
    # The location of the root directory to extract videos from
    root_dir = r"C:\video_clips"
    for camera_dir in Path(root_dir).iterdir():
        init_num = -1
        for datetime_dir in camera_dir.iterdir():
            for video_file_path in datetime_dir.iterdir():
                # If the file is a hidden file
                if video_file_path.stem[0] == ".":
                    continue
                else:
                    init_num +=1
                # cv2.VideoCapture requires a string argument
                video_file = str(video_file_path)

                if init_num%INTERVAL_CLIP == 0:
                    print('this is number {} clips, the path is {}'.format(init_num,video_file))
                    captured_video = cv2.VideoCapture(video_file)

                    # Gets the frames per second of this file
                    fps = captured_video.get(cv2.CAP_PROP_FPS)

                    interval_frames = INTERVAL_FRAME * fps

                    frame_no = -1
                    while captured_video.isOpened():
                        read_successful, frame = captured_video.read()

                        # Stop reading if failed this frame
                        if not read_successful:
                            break

                        frame_no += 1
                        if frame_no % interval_frames == 0:

                            # Output
                            img_file = str(os.path.join(
                                output_dir,
                                camera_dir.stem + "_" + datetime_dir.stem + "_" \
                                    + Path(video_file).stem + "_" + str(frame_no) \
                                    + ".jpg"
                            ))
                            cv2.imwrite(img_file, frame)


if __name__ == "__main__":
    main()
