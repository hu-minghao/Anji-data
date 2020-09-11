# python3 extractor.py
import os
import cv2
from pathlib import Path


INTERVAL = 10.0  # time interval for extracting a frame (secs)


def main():
    # The output dir for storing the extracted imgs
    output_dir = "bmw_extracted"
    os.makedirs(output_dir, exist_ok=True)

    # The location of the root directory to extract videos from
    root_dir = "/workspace/video_clips"

    for camera_dir in Path(root_dir).iterdir():
        for datetime_dir in camera_dir.iterdir():
            for video_file_path in datetime_dir.iterdir():
                # If the file is a hidden file
                if video_file_path.stem[0] == ".":
                    continue

                # cv2.VideoCapture requires a string argument
                video_file = str(video_file_path)

                captured_video = cv2.VideoCapture(video_file)

                # Gets the frames per second of this file
                fps = captured_video.get(cv2.CAP_PROP_FPS)

                interval_frames = INTERVAL * fps

                frame_no = 0
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
