##深度学习过程中，需要制作训练集和验证集、测试集。

import os, random, shutil
import argparse
from pathlib import Path
from tqdm import tqdm

def set_up_argument(parser):
    parser.add_argument('sourceFileDir',
                        type=str,
                        help='filedir of source frame')

    parser.add_argument('saveResultDir',
                        type=str,
                        help='filedir of save result')

    parser.add_argument('-n',
                        dest='select_number',
                        help='number of frame select from source frame'
                        )

    args = parser.parse_args()

    return args

def moveFile(fileDir,output_dir):
    pathDir = os.listdir(fileDir)  # 取图片的原始路径
    os.makedirs(output_dir, exist_ok=True)
    if type(sn)==int:
        picknumber = sn # sn为整数，则抽取相应数量的图图片
    if type(sn)==float:
        filenumber = len(pathDir)
        rate = sn  # 自定义抽取图片的比例，sn为浮点型，则抽取相应比例的图片。
        picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片

    sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片

    for name in tqdm(sample):
        move_Dir, tar_Dir = Path(fileDir, name), Path(tarDir, name)
        shutil.move(move_Dir, tar_Dir)
    return


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser('select frame from source dir')
    select_args = set_up_argument(my_parser)
    fileDir = select_args.sourceFileDir  # 源图片文件夹路径
    tarDir = select_args.saveResultDir  # 移动到新的文件夹路径
    sn = select_args.select_number
    moveFile(fileDir, tarDir)
















