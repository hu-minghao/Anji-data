import os
import xml.dom.minidom
import cv2 as cv

ImgPath = r'D:\data\honglu_labled\head_data'
AnnoPath = r'C:\Users\TangChun\Downloads\安吉交付数据-9.23(1)\XML\\honglu_traindata_8_12'

imagelist = os.listdir(ImgPath)
for image in imagelist:

    image_pre, ext = os.path.splitext(image)
    imgfile = ImgPath + '\\' + image
    print('1',imgfile)
    camera_dir = image.split('_')[0]
    xmlfile = os.path.join(AnnoPath, camera_dir) + '\\' + image_pre + '.xml'
    # 打开xml文档
    DOMTree = xml.dom.minidom.parse(xmlfile)
    # 得到文档元素对象
    collection = DOMTree.documentElement
    # 读取图片
    img = cv.imread(imgfile)

    filenamelist = collection.getElementsByTagName("filename")
    filename = filenamelist[0].childNodes[0].data
    print(filename)
    # 得到标签名为object的信息
    objectlist = collection.getElementsByTagName("object")

    for objects in objectlist:
        # 每个object中得到子标签名为name的信息
        namelist = objects.getElementsByTagName('name')
        # 通过此语句得到具体的某个name的值
        objectname = namelist[0].childNodes[0].data
        if objectname == 'head':
            bndbox = objects.getElementsByTagName('bndbox')
            for box in bndbox:
                x1_list = box.getElementsByTagName('xmin')
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = box.getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = box.getElementsByTagName('xmax')
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = box.getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
                cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
                cv.putText(img, objectname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                           thickness=2)
                cv.imshow('head', img)
                out_put_dir = os.path.join(r"D:\data\honglu_labled\head_data_labeled", image)
            cv.imwrite(out_put_dir, img)   #save picture