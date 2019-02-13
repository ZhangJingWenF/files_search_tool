#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhangjingwen
@contact: xdzhangjingwen@163.com
@software: PyCharm
@file: solution.py
@time: 2019/1/24 19:22
"""
from pathlib import Path


class Search():
    def __init__(self):
        self.init_path = 'F:\Python学习笔记'
        self.file_list = []
        self.dir_list = []
        self.result_count = 0
        self.dest_file = []
        self.dest_dir = []
        self.fileANDdir = []

    def try_connect_ftp(self, path: str, init_dir: str):
        """判断文件服务器是否连接OK"""
        init_path = Path(path+init_dir)
        if init_path.exists():
            self.init_path = init_path
            return True
        else:
            return

    def search_all(self, only_file=False, only_dir=False):
        """遍历所有文件夹，将文件和文件夹分别存放"""
        def _recursion_search(p: Path):
            """递归遍历所有文件夹"""
            if not p.is_dir():
                return
            for file in p.iterdir():
                try:
                    if file.is_dir():
                        self.dir_list.append(file)
                        _recursion_search(file)
                    elif file.is_file():
                        self.file_list.append(file)
                except PermissionError:
                    continue
            return

        self.file_list = []
        self.dir_list = []
        if self.init_path:
            p = Path(self.init_path)
            try:
                if p.is_dir():
                    self.dir_list.append(p)
                    _recursion_search(p)
                elif p.is_file():
                    self.file_list.append(p)
            except PermissionError:
                return

        if only_file is True and only_dir is False:
            yield from self.file_list
        elif only_file is False and only_dir is True:
            yield from self.dir_list
        else:
            yield from self.file_list+self.dir_list

    def search_file(self, file_keyword: str):
        """仅搜索所有文件"""
        self.dest_file = []
        self.result_count = 0
        result = self.search_all(only_file=True)
        for file in result:
            if file_keyword in str(file.name) and file_keyword != '':
                self.dest_file.append(file)
                self.result_count += 1
        yield from self.dest_file

    def search_dir(self, dir_keyword: str):
        """仅搜索所有文件夹"""
        self.dest_dir = []
        self.result_count = 0
        result = self.search_all(only_dir=True)
        for dir in result:
            if dir_keyword in str(dir.name) and dir_keyword != '':
                self.dest_dir.append(dir)
                self.result_count += 1
        yield from self.dest_dir

    def search_fileANDdir(self, *keyword: str):
        """混合搜索"""
        self.fileANDdir = []
        self.result_count = 0
        result = self.search_all()
        for x in result:
            for y in keyword:
                if y in str(x.name) and y != '':
                    self.fileANDdir.append(x)
                    self.result_count += 1
        yield from self.fileANDdir

