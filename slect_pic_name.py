from pathlib import Path
import os

pic_dir = r'D:\data\honglu_labled\head_data_error'
pic_path = Path(pic_dir)

with open(r'D:\data\honglu_labled\head_error.txt', 'a') as f:
    for img in pic_path.iterdir():
        img_name = img.name
        f.write('\n'+img_name)
    f.close()