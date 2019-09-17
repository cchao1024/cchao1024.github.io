#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

root_path = '/Users/cchao/github/hexo/source/_post'

def rename(item, old_str, new_str):
    if os.path.splitext(item)[1] != '.md':
        return
    print('文件名：' + os.path.join(root_path, item))
    file_data = ""
    with open(os.path.join(root_path, item), "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
        with open(os.path.join(root_path, item), "w", encoding="utf-8") as f:
            f.write(file_data)


for (root, dirs, files) in os.walk(root_path):
    for item_file in files:
        rename(item_file, '](../../images/', '](../../images/')
