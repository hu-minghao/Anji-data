import os
import cv2
from pathlib import Path

INTERVAL = 30 # time interval for extracting a frame (secs)


def main():
    # The output dir for storing the extracted imgs
    output_dir = r"C:\extractor_test\result2"
    os.makedirs(output_dir, exist_ok=True)
    # The location of the root directory to extract videos from
    root_dir = r"C:\extractor_test\data_process_test1"
    # 可以继续添加需要的格式
    video_style = {'.mp4', '.avi'}
    init_time = 0.0
    clip_id = 0
    for root, dirs, files in os.walk(root_dir):
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
            clip_id += 1
            # 打开视频
            captured_video = cv2.VideoCapture(video_file)
            if captured_video.isOpened():  # 当成功打开视频时.isOpened()返回True,否则返回False
                rate = captured_video.get(cv2.CAP_PROP_FPS)  # 帧速率
                FrameNumber = captured_video.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频文件的帧数
                duration = FrameNumber / rate   # 帧速率/视频总帧数 单位为秒
            else:
                continue

            temp = init_time//INTERVAL
            # 处理间隔时间原小于视频长度的长视频，处理速度会较慢，而处理filter收集的数据会很快，根据间隔时间
            # 会跳过相应数量的帧
            if duration < (temp + 1)*INTERVAL - init_time:
                init_time += duration
                print(video_file_path)
                print('add time,then pass', init_time)
                continue

            # 给每一个clip一个编号
            get_frame_no = {}
            frame_no = -1
            while captured_video.isOpened():
                read_successful, frame = captured_video.read()
                # Stop reading if failed this frame
                if not read_successful:
                    break

                frame_no += 1
                # 该帧所在时间点
                frame_no_time = frame_no*(1/rate)
                init_no_time = init_time + frame_no_time
                print(frame_no)
                if init_no_time % INTERVAL <= 0.12:
                    print('good for select, diff:{},init_no_time:{}'.format(init_no_time % INTERVAL, init_no_time))
                    old_frame_no = get_frame_no.setdefault(clip_id, 0)
                    print('clip_id', clip_id, old_frame_no)
                    if frame_no - old_frame_no < 2:
                        print('#66', frame_no-old_frame_no)
                        continue
                    else:
                        get_frame_no[clip_id] = frame_no
                        print('get_frame_no,clip {},old_frame_no:{}'.format(clip_id,frame_no))
                    # Output
                    img_file = str(os.path.join(
                        output_dir,
                        Path(video_file).stem + "_" + str(frame_no) \
                        + ".jpg"
                    ))
                    cv2.imwrite(img_file, frame)
                    print(init_no_time)
                    print('write')
                else:
                    print('bad for select, diff:{},init_no_time:{}'.format(init_no_time % INTERVAL, init_no_time))
            init_time += duration


if __name__ == "__main__":
    main()
