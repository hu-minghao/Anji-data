##可以从图片中筛选出固定数量或者一定比例的图片

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

def moveFile(fileDir,output_dir,sn):
    picknumber = 0
    pathDir = os.listdir(fileDir)  # 取图片的原始路径
    #print(pathDir)
    os.makedirs(output_dir, exist_ok=True)
    #print(output_dir)
    if sn[0]!='0':
        picknumber = int(sn) # sn为整数，则抽取相应数量的图图片
    if sn[0]=='0':
        filenumber = len(pathDir)
        rate = float(sn)  # 自定义抽取图片的比例，sn为浮点型，则抽取相应比例的图片。
        picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
    print("从{}张图中共抽取{}张图片".format(len(pathDir),picknumber))
    sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片
    #print(sample)
    for name in tqdm(sample):
        move_Dir, tar_Dir = Path(fileDir, name), Path(tarDir, name)
        shutil.move(move_Dir, tar_Dir)
    print('Done!')
    return


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser('select frame from source dir')
    select_args = set_up_argument(my_parser)
    fileDir = select_args.sourceFileDir  # 源图片文件夹路径
    tarDir = select_args.saveResultDir  # 移动到新的文件夹路径
    sn = select_args.select_number
    #print(fileDir,tarDir,sn)
    #print(type(sn))
    moveFile(fileDir, tarDir, sn)
















