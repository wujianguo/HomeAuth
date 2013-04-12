#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: UTF-8 -*-

# face_detect.py

# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b

# Usage: python face_detect.py <image_file>

import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
from PIL import Image, ImageDraw
import cv

def detect_object(image):
    '''检测图片，获取人脸在图片中的坐标'''
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    cascade = cv.Load(os.path.join(ROOT_DIR,"haarcascade_frontalface_alt_tree.xml"))
    rect = cv.HaarDetectObjects(grayscale, cascade, cv.CreateMemStorage(), 1.1, 3,
        cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))

    result = []
    for r in rect:
        result.append((r[0][0], r[0][1], r[0][0]+r[0][2], r[0][1]+r[0][3]))

    return result

def process(infile):
    '''在原图上框出头像并且截取每个头像到单独文件夹'''
    image = cv.LoadImage(infile);
    if image:
        faces = detect_object(image)

    im = Image.open(infile)
    path = os.path.abspath(infile)
    save_path = os.path.splitext(path)[0]+"_face"
    try:
        os.mkdir(save_path)
    except:
        pass
    if faces:
        draw = ImageDraw.Draw(im)
        count = 0
        for f in faces:
            count += 1
            draw.rectangle(f, outline=(255, 0, 0))
            a = im.crop(f)
            file_name = os.path.join(save_path,str(count)+".jpg")
     #       print file_name
            a.save(file_name)

        drow_save_path = os.path.join(save_path,"out.jpg")
        print(drow_save_path)
        im.save(drow_save_path, "JPEG", quality=80)
    else:
        print "Error: cannot detect faces on %s" % infile
if __name__ == "__main__":
    
    process(os.path.join(ROOT_DIR,'input.jpg'))