import os
import cv2
import argparse
from pathlib import Path


def set_up_argument(parser):
    parser.add_argument('rootDir',
                        type=str,
                        help='The location of the root directory to extract videos from')

    parser.add_argument('outputDir',
                        type=str,
                        help='The output dir for storing the extracted imgs')

    parser.add_argument('-i',
                        dest='INTERVAL',
                        type=int,
                        default=10,
                        help='time interval for extracting a frame (secs)'
                        )

    args = parser.parse_args()

    return args


def main():
    # 给一个文件夹，装任意视频文件，抽取为视频等时长间隔的图片，这里的时间间隔以视频时长为基础
    extractor_parse = argparse.ArgumentParser("Extract frames at regular intervals")
    args = set_up_argument(extractor_parse)
    interval = args.INTERVAL
    output_dir = args.outputDir
    os.makedirs(output_dir, exist_ok=True)
    # The location of the root directory to extract videos from
    root_dir = args.rootDir
    # 可以继续添加需要的格式
    video_style = {'.mp4', '.avi', '.wmv', '.mpeg', '.m4v','.mov', '.flv', '.f4v', '.rmvb', '.3gp', '.vob'}

    # 初始化起点
    init_time = 0.0
    clip_id = 0

    # 处理的图片数量
    frame_num  = 0

    for root, dirs, files in os.walk(root_dir):
        # 查找所有的视频文件
        for name in files:
            video_file_path = Path(os.path.join(root, name))
            # 跳过隐藏文件与非视频格式文件
            if video_file_path.stem[0] == ".":
                continue
            if video_file_path.suffix not in video_style:
                continue

            clip_id += 1
            # cv2.VideoCapture requires a string argument
            video_file = str(video_file_path)
            # 打开视频
            captured_video = cv2.VideoCapture(video_file)

            if captured_video.isOpened():  # 当成功打开视频时.isOpened()返回True,否则返回False
                rate = captured_video.get(cv2.CAP_PROP_FPS)  # 帧速率
                frame_number = captured_video.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频文件的帧数
                duration = frame_number / rate   # 帧速率/视频总帧数 单位为秒
            else:
                continue

            print('{}th clips, cumulative frame{}'.format(clip_id, frame_num))

            # 根据间隔时间,跳过相应数量的帧
            # 处理长视频，处理速度会较慢，而处理filter收集的1s clip会很快
            turn_num = init_time//interval
            if duration < (turn_num + 1)*interval - init_time:
                init_time += duration
                continue

            # 记录上一帧位置，放在这里可以节省一点内存空间
            get_frame_no = {}
            frame_no = -1

            # 循环读取帧
            while captured_video.isOpened():
                read_successful, frame = captured_video.read()
                # Stop reading if failed this frame
                if not read_successful:
                    break

                frame_no += 1

                # 该帧所在时间点
                frame_no_time = frame_no*(1/rate)
                init_no_time = init_time + frame_no_time

                # 防止重复抽取，间隔至少为3帧
                if init_no_time % interval <= 0.12:
                    frame_num += 1
                    # print('The appropriate frame, diff:{},The cumulative frame:{}'.format(init_no_time % interval, frame_num))
                    old_frame_no = get_frame_no.setdefault(clip_id, 0)
                    if frame_no - old_frame_no < 2:
                        continue
                    else:
                        get_frame_no[clip_id] = frame_no

                    # Output
                    img_file = str(os.path.join(
                        output_dir,
                        Path(video_file).stem + "_" + str(frame_no) \
                        + ".jpg"
                    ))
                    cv2.imwrite(img_file, frame)
                # else:
                #     print('Inappropriate frame, diff:{},The cumulative time:{}'.format(init_no_time % interval, init_no_time))
            # 记录累计视频时长
            init_time += duration
    print('Done!')
    print('the total of {} pictures were taken.'.format(frame_num))


if __name__ == "__main__":
    main()
