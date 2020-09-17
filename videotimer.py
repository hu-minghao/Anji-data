# python3 extractor_new.py
import os
import cv2
from pathlib import Path
from videoselector import VideoSelector


class Dater:

    def __init__(self, root_dir):
        # The location of the root directory to extract videos from
        # the total dir struct is like this : root_dir/camerax/202009080001/xxx.mp4
        # 将每个摄像头采集数据的日期保存为字典
        self.date = dict()
        for camera_dir in Path(root_dir).iterdir():
            camera_date = set()
            for datetime_dir in camera_dir.iterdir():
                if Path(datetime_dir).is_dir():
                    datetime = datetime_dir.name[:8]
                    camera_date.add(datetime)
            self.date[camera_dir.name] = list(camera_date)

    def Start_end_date(self, camera_id):
        camera_dates = []
        camera_date = self.date[camera_id]
        for date in camera_date:
            start_date = int(str(int(date) - 1)+ '2300')
            end_date = int(date + '1100')
            camera_dates.append((start_date, end_date))
        return camera_dates




class Selector:

    def __init__(self, date_dir):
        # date_dir的绝对路径
        self.length = len(os.listdir(date_dir))
        self.dir = date_dir

    def get_best_frame_path(self):
        # 根据一分钟内采集的clips数量，选择抽取的clips数量
        # 一个文件夹内frame时间间隔为1s，一个文件夹时间间隔为1分钟
        # 以下标准,按有效数据的最低采集间隔为10s制定
        # 根据clips数量，将采集策略分为四种情况
        # 小于等于10，采取中位点的一个clip
        # 大于10，小于等于20，采取尽可能中间，但间隔保持10s的两个clip
        # 大于20，小于40，取0.25，0.75分位点的两个clip
        # 大于等于40，取0.17，0.5，0.83分位点的三个clip
        select_video_file_list = []
        vs = VideoSelector(self.dir)
        if self.length <= 10:
            select_video_file_list.append(vs.quentile(0.5))
        elif (self.length > 10) and (self.length <=20):
            left_place = int((self.length - 10)/2)
            select_video_file_list.append(vs.index(left_place))
            select_video_file_list.append(vs.index(left_place+10))
        elif (self.length > 20) and (self.length < 40):
            select_video_file_list.append(vs.quentile(0.25))
            select_video_file_list.append(vs.quentile(0.75))
        elif self.length >= 40:
            select_video_file_list.append(vs.quentile(0.17))
            select_video_file_list.append(vs.quentile(0.5))
            select_video_file_list.append(vs.quentile(0.83))

        return select_video_file_list


# camera_path = r'C:\video_clips'
# honglu_camera = Dater(camera_path)
#
# print(honglu_camera.date)
# camera_date = honglu_camera.Start_end_date('camera7')
# print(camera_date)