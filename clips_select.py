# python3 extractor.py
import os
import cv2
import numpy as np
from scipy import stats
from pathlib import Path


def main():
    num_imgs = 50000
    # The output dir for storing the extracted imgs
    output_dir = "extracted"
    os.makedirs(output_dir, exist_ok=True)

    # The location of the root directory to extract videos from
    root_dir = "data"

    num_total_frames = 0  # accumulated total frames
    record_total_frames = []  # list of total frames
    video_files = []  # list of video files
    for video_dir in Path(root_dir).iterdir():
        for video_file_path in video_dir.iterdir():
            # If the file is a hidden file
            if video_file_path.stem[0] == ".":
                continue

            # cv2.VideoCapture requires a string argument
            video_file = str(video_file_path)
            video_files.append(video_file)

            captured_video = cv2.VideoCapture(video_file)

            # Type convert: float -> int
            num_frames = int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT))  # total frames

            record_total_frames.append(num_frames)
            num_total_frames += num_frames

    pr_dist = [total_frames / num_total_frames for total_frames in record_total_frames]  # probability distribution

    # Construct specific distribution for discrete random variables
    rnd_gen = stats.rv_discrete(
        values=(np.arange(len(record_total_frames)), pr_dist)
    )
    # Count number of occurrences of each value in array of non-negative ints
    counters = np.bincount(rnd_gen.rvs(size=num_imgs))

    # Add zeros for the tailing missing values of 'counters'
    if len(video_files) != len(counters):
        for i in range(len(video_files) - len(counters)):
            counters = np.append(counters, 0)

    for video_file, num_frames in zip(video_files, counters):
        captured_video = cv2.VideoCapture(video_file)

        # Type convert: float -> int
        num_frames = int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT))  # total frames

        # The No. of frames to read
        frame_nos = np.random.choice(num_frames, num_frames, replace=False)

        for frame_no in frame_nos:
            # Setting the next frame to read
            captured_video.set(cv2.CAP_PROP_POS_FRAMES, frame_no)

            # Extraction
            did_read_frame, img = captured_video.read()

            assert did_read_frame, "Read frame failed."

            # Output
            img_file = str(os.path.join(
                output_dir,
                Path(video_file).stem + "_" + str(frame_no) + ".jpg"
            ))
            cv2.imwrite(img_file, img)


if __name__ == "__main__":
    main()
