#  !/usr/bin/env  python
#  -*- coding:utf-8 -*-
# @Time   :  2025.01
# @Author :  绿色羽毛
# @Email  :  lvseyumao@foxmail.com
# @Blog   :  https://blog.csdn.net/ViatorSun
# @Note   :


import os
import os.path as osp
import json
from PIL import Image
import numpy as np

suffix_lst = [".jpg", ".jpeg", ".png"]

def read_json(json_dir):
    """ 从标注文件中提取出每个标注框的左上、右下点坐标
    :param json_dir: 标注文件路径
    :return: class，min_x, min_y, max_x, max_y
    """
    with open(json_dir, 'r') as file:
        json_data = json.load(file)

        data_lst = json_data[-1]["instances"]
        coord_lst = []

        for data in data_lst:
            clas = data["ClassID"]
            coordinates = data["Vertices"]

            # 提取所有的 x 和 y 坐标
            x_values = [point[0] for point in coordinates]
            y_values = [point[1] for point in coordinates]

            # 计算最小和最大值
            min_x = min(x_values)
            min_y = min(y_values)
            max_x = max(x_values)
            max_y = max(y_values)

            # coord_lst.append([clas, min_x, min_y, max_x, max_y])

            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            width = max_x - min_x
            height = max_y - min_y

            coord_lst.append([clas, center_x, center_y, width, height])


    return coord_lst


def coord2yolo():

    return []


def batch_convert(imges_dir, anns_dir, save_dir):
    """ 批量将数据从json格式转化为 yolo格式
    :param imges_dir: 图片数据所在路径
    :param anns_dir: json标注数据路径
    :param save_dir: 新保存的yolo格式路径
    :return: None
    """

    # 遍历所有的数据
    for root, dirs, files in os.walk(imges_dir):
        for file in files:
            suffix = osp.splitext(file)[-1]
            if suffix.lower() in suffix_lst:
                img_dir = osp.join(root, file)
                json_dir = (anns_dir + img_dir[len(imges_dir):]).replace(suffix, ".json")
                txt_dir = (save_dir + img_dir[len(imges_dir):]).replace(suffix, ".txt")

                with Image.open(img_dir) as img:
                    # 获取图片的宽度和高度
                    img_width, img_height = img.size

                if not osp.exists(json_dir):
                    continue

                coord_lst = read_json(json_dir)


                if not osp.exists(osp.dirname(txt_dir)):
                    os.makedirs(osp.dirname(txt_dir))

                with open(txt_dir, 'w') as f:
                    for coords in coord_lst:
                        # class_id, *box = coords     # box: min_x, min_y, max_x, max_y
                        class_id, center_x, center_y, width, height = coords     # center_x, center_y, width, height

                        center_x /= img_width
                        center_y /= img_height
                        width /= img_width
                        height /= img_height

                        if width > 0.0 and height > 0.0:  # if w > 0 and h > 0
                            f.write("{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(class_id, center_x, center_y, width, height))

                print(f"handle file: {txt_dir}")




if __name__ == '__main__':

    imges_dir = "/outsun/project"
    anns_dir = "/outsun/annotation"
    save_dir = "/outsun/yolo"


    # json_dir = "/Users/viatorsun/Desktop/Demo/VLM/outsun/annotation/044C00312024121713442586_2/3d3d3347a838f40680248b02c175e2d2.json"

    # read_json(json_dir)

    batch_convert(imges_dir, anns_dir, save_dir)

