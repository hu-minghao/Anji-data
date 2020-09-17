import os


class VideoSelector:

    def __init__(self, datetime_dir):
        # date_time的绝对路径
        self.list = os.listdir(datetime_dir)

        def takeindex(elem):
            split_list = elem.split('_', 3)
            clip_index = int(split_list[2])
            return clip_index
        self.list.sort(key=takeindex)
        #print(self.list)

    def quentile(self, quannum):
        video_length = len(self.list)
        quantile_num = int(video_length*quannum + 0.5)
        return self.list[quantile_num]

    def index(self, index):
        return self.list[index]

#date_file = VideoSelector(r'C:\camera\camera7\202009150244')
#print(date_file.list)
#print(date_file.quentile(0.5))