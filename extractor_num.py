import cv2
from pathlib import Path
from interval import Interval
import os

select_dic = {'camera3':[20200917], 'camera26':[20200916, 20200918]}

root_dir = 'C:/camera7/video_clips'
video_dir = Path(root_dir)
for camera_dir in video_dir.iterdir():
    if camera_dir.name in select_dic.key():
        time_interval_list = []
        for date in select_dic[camera_dir.name]:
            # 采集时间为上午六点，到下午七点（13个小时）
            start_time , end_time = str(date - 1) + '2200', str(date) + '1100'
            time_interval = Interval.between(int(start_time), int(end_time))
            time_interval_list.append(time_interval)
            select_time = IntervalSet(time_interval_list)

