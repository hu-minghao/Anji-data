import os
import cv2
from pathlib import Path

INTERVAL = 30 # time interval for extracting a frame (secs)


def main():
    # The output dir for storing the extracted imgs
    output_dir = r"C:\data\result"
    os.makedirs(output_dir, exist_ok=True)
    # The location of the root directory to extract videos from
    root_dir = r"C:\data_process_test"
    video_style = {'.mp4','.avi'}
    init_time = 0.0
    for root, dirs, files in os.walk(root_dir, topdown = True):
        # 先查找视频文件
        for name in files:
            video_file_path = Path(os.path.join(root, name))
            if video_file_path.stem[0] == ".":
                continue
            if video_file_path.suffix not in video_style:
                continue
            print(video_file_path)

            # cv2.VideoCapture requires a string argument
            video_file = str(video_file_path)
            # 打开视频
            captured_video = cv2.VideoCapture(video_file)
            if captured_video.isOpened():  # 当成功打开视频时.isOpened()返回True,否则返回False
                # get方法参数按顺序对应下表（从0开始编号)
                rate = captured_video.get(cv2.CAP_PROP_FPS)  # 帧速率
                FrameNumber = captured_video.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频文件的帧数
                duration = FrameNumber / rate   # 帧速率/视频总帧数 单位为秒
            else:
                continue

            temp = init_time//INTERVAL
            if abs(INTERVAL -duration) > abs(init_time-temp*INTERVAL):
                init_time += duration
                continue

            frame_no = -1
            while captured_video.isOpened():
                read_successful, frame = captured_video.read()
                # Stop reading if failed this frame
                if not read_successful:
                    break

                frame_no += 1
                # 该帧所在时间点
                frame_no_time = frame_no*(1/rate)

                init_no_time =init_time + frame_no_time

                if init_no_time % INTERVAL <= 0.05:
                    # Output
                    print(init_no_time)
                    img_file = str(os.path.join(
                        output_dir,
                        Path(video_file).stem + "_" + str(frame_no) \
                        + ".jpg"
                    ))
                    cv2.imwrite(img_file, frame)
            init_time += duration
            print(init_time)


if __name__ == "__main__":
    main()
