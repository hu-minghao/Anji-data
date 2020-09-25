# python3 extractor_new.py
import os
import cv2
from pathlib import Path
from videotimer import Dater

INTERVAL_CLIP = 10  # clip interval for extracting a frame (secs)
INTERVAL_FRAME = 1  # time interval for extracting a frame (secs)


def main():

    # The location of the root directory to extract videos from
    root_dir = r"C:\video_clips"
    select_camera = {'camera30', 'camera31', 'camera29', 'camera32'}
    camera_date_select = Dater(root_dir).date
    for camera in camera_date_select:
        print('get clip from {} in {}'.format(camera, camera_date_select[camera]))

    # The output dir for storing the extracted imgs
    output_dir = r"C:\video_clips\result"
    os.makedirs(output_dir, exist_ok=True)
    # start_time, end_time = 202009150300, 202009150305
    init_num = -1
    for camera_dir in Path(root_dir).iterdir():
        print('camera name',camera_dir.name)
        if camera_dir.name in select_camera:
            for datetime_dir in camera_dir.iterdir():
                if Path(datetime_dir).is_dir():
                    dir_time = int(datetime_dir.name[-4:])
                else:
                    continue
                if (dir_time >= 2300) or (dir_time <= 1100):
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
        else:
            continue


if __name__ == "__main__":
    main()
