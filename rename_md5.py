#  !/usr/bin/env  python
#  -*- coding:utf-8 -*-
# @Time   :  2025.01
# @Author :  绿色羽毛
# @Email  :  lvseyumao@foxmail.com
# @Blog   :  https://blog.csdn.net/ViatorSun
# @Note   :


import os
import os.path as osp

suffix_lst = [".jpg", ".jpeg", ".png"]

imges_dir = "/home/sun/Zhiwei/Dataset/out/project"
anns_dir = "/home/sun/Zhiwei/Dataset/out/annotation"

for root, dirs, files in os.walk(imges_dir):
    for file in files:
        suffix = osp.splitext(file)[-1]

        if suffix.lower() in suffix_lst:
            img_dir = osp.join(root, file)
            ann_file_dir = anns_dir + img_dir[len(imges_dir):]
            ann_file_dir = ann_file_dir.replace(suffix, ".json")

            cmd = f"md5sum  '{img_dir}'"
            md5 = "".join(os.popen(cmd).readlines())
            md5value = md5.split(" ")[0]

            new_img = osp.join(root, md5value + suffix)
            new_ann = osp.join(osp.dirname(ann_file_dir), md5value + ".json")

            if img_dir == new_img:
                continue

            os.system("mv '{}' '{}'".format(img_dir, new_img))
            print(f"mv {md5value} {img_dir}")

            if osp.exists(ann_file_dir):
                os.system("mv '{}' '{}'".format(ann_file_dir, new_ann))
                print(f"mv {md5value} {new_ann}\n")





