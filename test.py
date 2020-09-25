from xml.dom.minidom import parse

import os
from pathlib import Path
import shutil

def check_tag(file_path,interest_tag):
    num = 0
    dom = parse(file_path)
    root = dom.documentElement
    file_name = root.getElementsByTagName('filename')[0].childNodes[0].nodeValue
    folder = root.getElementsByTagName('folder')[0].childNodes[0].nodeValue
    camera_folder = folder.split('/')[1]
    # img_file = os.path.join(folder, file_name)
    all_tags = root.getElementsByTagName('name')
    # print(len(all_tags))
    for tag in all_tags:
        if tag.childNodes[0].nodeValue == interest_tag:
            num += 1
    return num, file_name, camera_folder


# num, file, folder = check_tag(img_path, 'head')
# print(num, file, folder)
root_dir = r'C:\Users\TangChun\Downloads\安吉交付数据-9.23(1)\XML\honglu_traindata_8_12'
output_dir = r'D:\data\honglu_labled\head_data'
total_num = 0
camera_dir = Path(root_dir)
for camera in camera_dir.iterdir():
    for img in camera.iterdir():
        img_file_path = str(img)
        num, file, cameraDir = check_tag(img_file_path, 'helmet')
        if num > 0:
            total_num += num
            # img_file = os.path.join(r'C:\Users\TangChun\Downloads\安吉交付数据-9.23(1)\图片\honglu_traindata_8_12', cameraDir)+'\\'+ img.stem + '.jpg'
            # out_path = os.path.join(output_dir,img.stem) + '.jpg'
            # shutil.copy(img_file, out_path)

print(total_num)





