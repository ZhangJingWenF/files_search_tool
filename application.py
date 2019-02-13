#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhangjingwen
@contact: xdzhangjingwen@163.com
@software: PyCharm
@file: application.py
@time: 2019/1/24 19:21
"""

import os
import solution
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.menubar = tk.Menu(self.master)  # 添加菜单
        self.adds = Address()
        self.create_widgets()

        self.solution = solution.Search()    # 实例化搜索类，实现单例

    def create_widgets(self):
        """创建窗口基础控件"""
        tk.Label(text='当前服务器地址:').grid(row=0, sticky='W', columnspan=2)
        tk.Label(text='请输入文件名/关键字 :').grid(row=1, sticky='W', columnspan=2)
        tk.Label(self.master, text='请输入文件夹名/关键字:').grid(row=2, sticky='W', columnspan=2)
        self.show_address = tk.Label(text=self.adds.adds, fg='green')
        self.show_address.grid(row=0, column=2, sticky='W', columnspan=2)
        self.tips =tk.Label(text=r'Tips:等待搜索...')
        self.tips.grid(row=5, column=0, sticky='W', columnspan=2, pady=5)

        # 关键字输入框
        self.entry1 = tk.Entry(bg='white', takefocus=1)
        self.entry1.focus_set()
        self.entry2 = tk.Entry(self.master, bg='white', takefocus=1)

        # checkButton
        self.var = tk.IntVar()
        self.no_limit = tk.Radiobutton(text='全部搜索', variable=self.var, value=1)
        self.only_file = tk.Radiobutton(text='仅搜索文件', variable=self.var, value=2)
        self.only_dir = tk.Radiobutton(text='仅搜索文件夹', variable=self.var, value=3)

        # 创建按钮
        self.find = tk.Button(text='搜    索', fg='green', relief='raised', command=self.create_resultWindow)
        self.exit = tk.Button(text='退    出', fg='red', command=self.master.destroy)
        self.change = tk.Button(text='更改地址', fg='green', command=self.create_reset_adds)

        # 事件绑定
        self.master.bind('<Return>', self.create_resultWindow)

        self.entry1.grid(row=1, column=2, columnspan=2)
        self.entry2.grid(row=2, column=2, columnspan=2)
        self.find.grid(row=4, column=0, sticky='E', columnspan=2, padx=18, pady=2)
        self.change.grid(row=4, column=2, sticky='W', columnspan=2, padx=33, pady=2)
        self.exit.grid(row=4, column=3, sticky='E', columnspan=2, pady=2)
        self.no_limit.grid(row=0, column=4, sticky='W', columnspan=2)
        self.only_file.grid(row=1, column=4, sticky='W', columnspan=2)
        self.only_dir.grid(row=2, column=4, columnspan=2)

    def add_menu(self, Menu):
        """添加菜单"""
        Menu(self)
        self.master.config(menu=self.menubar)

    def create_reset_adds(self):
        """创建重设服务器地址窗口"""
        self.top = tk.Toplevel()
        self.top.grab_set()
        self.top.focus_set()
        self.top.title('更改服务器地址')
        width = int((self.master.winfo_screenwidth()-280)/2)
        height = int((self.master.winfo_screenheight()-100)/2)
        self.top.geometry('280x120+{}+{}'.format(width, height))
        self.top.resizable(False, False)
        self.top.bind('<Return>', self.reset_adds)

        tk.Label(self.top, text='请输入新服务器地址：').grid(row=0, column=1, columnspan=2, sticky='W', padx=38, pady=5)
        tk.Label(self.top, text='Tips: 地址格式为 \\\\x.x.x.x').grid(row=3, column=0, columnspan=2, sticky='W')
        self.new_adds = tk.Entry(self.top, bg='white', takefocus=1, width=28)
        self.new_adds.focus_set()
        self.new_adds.grid(row=1, column=1, columnspan=2, sticky='S', padx=40)
        tk.Button(self.top, text='确   定', command=self.reset_adds, fg='green').grid(row=2, column=1,
                                                                                    sticky='E', pady=8, padx=15)
        tk.Button(self.top, text='取   消', command=self.top.destroy, fg='red').grid(row=2, column=2,
                                                                                    sticky='W', pady=8, padx=15)

    def reset_adds(self, event=None):
        """重设服务器地址，校验合法性"""
        try:
            tmp = self.new_adds.get().strip()
        except:
            tmp = ''
        if tmp != '':
            self.adds.change_adds(tmp)
            self.show_address['text'] = self.adds.adds
            self.show_address['fg'] = 'red' if self.adds.adds == '非法地址，请核对！' else 'green'
            self.master.update()
        self.top.destroy()

    def create_reset_sharedir(self):
        """创建更改共享文件夹弹窗"""
        self.top1 = tk.Toplevel()
        self.top1.focus_set()
        self.top1.grab_set()
        self.top1.title('更改共享文件夹')
        width = int((self.master.winfo_screenwidth() - 280) / 2)
        height = int((self.master.winfo_screenheight() - 100) / 2)
        self.top1.geometry('280x100+{}+{}'.format(width, height))
        self.top1.resizable(False, False)
        self.top1.bind('<Return>', self.reset_sharedir)

        tk.Label(self.top1, text='请输入新文件夹名：').grid(row=1, column=0, columnspan=2, sticky='W', pady=3)
        tk.Label(self.top1, text='当前共享文件夹：').grid(row=0, column=0, columnspan=2, sticky='W', pady=3)
        tk.Label(self.top1, text=self.adds.sharedir).grid(row=0, column=2, columnspan=2, sticky='W', pady=3)
        self.new_sharedir = tk.Entry(self.top1, bg='white', takefocus=1)
        self.new_sharedir.focus_set()
        self.new_sharedir.grid(row=1, column=2, columnspan=2, sticky='S', pady=3)
        tk.Button(self.top1, text='确   定', command=self.reset_sharedir, fg='green').grid(row=2, column=1,
                                                                                         sticky='E', pady=3)
        tk.Button(self.top1, text='取   消', command=self.top1.destroy, fg='red').grid(row=2, column=2,
                                                                                     sticky='W', pady=3, padx=45)

    def reset_sharedir(self, event=None):
        """重设共享文件夹"""
        try:
            tmp = self.new_sharedir.get().strip()
        except:
            tmp = ''
        if tmp != '':
            self.adds.change_sharedir(tmp)
        self.top1.destroy()

    def openfile(self):
        """打开"""
        self.file_opt = {'filetypes': [('all files', '.*'), ('text file', '.txt')],
                         'initialdir': r'C:\Users\Administrator\desktop',
                         'title': '打开'}
        filename = filedialog.askopenfile(mode='r', **self.file_opt)
        try:
            os.startfile(filename.name)
        except:
            pass

    def savefile(self):
        """文件另存为"""
        self.file_opt = {'filetypes': [('all files', '.*'), ('text file', '.txt')],
                         'initialdir': r'C:\Users\Administrator\desktop',
                         'title': '文件另存为'}
        filename = filedialog.asksaveasfilename(**self.file_opt)
        print(filename)

    def open_help(self):
        """打开帮助文档"""
        tmp = Path().cwd()
        try:
            os.startfile(str(tmp)+'\help.txt')
        except:
            messagebox.showinfo('错误', 'No such file!')

    def create_resultWindow(self, event=None):
        self.tips['text'] = 'Tips: 正在搜索...'
        self.master.update()                            # 更新主页面状态

        self.top3 = tk.Toplevel()
        self.top3.focus_set()                           # 将焦点转移到结果显示窗口，避免重复接收键盘enter事件
        self.top3.grab_set()                            # 当前窗口不关闭的情况下，禁止操作父窗口上的控件
        self.top3.title('搜索结果')
        width = int((self.master.winfo_screenwidth() - 550) / 2)
        height = int((self.master.winfo_screenheight() - 400) / 2)
        self.top3.geometry('550x400+{}+{}'.format(width, height))
        self.top3.resizable(True, False)                # 禁止纵向缩放

        self.top3.show = tk.Label(self.top3, fg='green',
                                  text='搜索完毕，已为您找到{}条结果:{}'.format(self.solution.result_count, ' '*93))
        self.top3.show.pack()
        yscroll = tk.Scrollbar(self.top3, orient=tk.VERTICAL)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        xscroll = tk.Scrollbar(self.top3, orient=tk.HORIZONTAL)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)                     # xy滚动轴

        var = tk.StringVar()
        my_listbox = tk.Listbox(self.top3, listvariable=var, height=200,
                                                             xscrollcommand=xscroll.set,
                                                             yscrollcommand=yscroll.set)
        my_listbox.pack(side='bottom', fill=tk.X)
        xscroll['command'] = my_listbox.xview
        yscroll['command'] = my_listbox.yview

        def open_item(*args):
            """将结果显示在listbox中"""
            items = my_listbox.curselection()
            for y in items:
                os.startfile(my_listbox.get(y))

        my_listbox.bind('<Double-Button-1>', open_item)  # 绑定鼠标双击事件

        dest = self.search()
        for i in dest:
            my_listbox.insert(tk.END, str(i))
        self.top3.show['text'] = '搜索完毕，已为您找到{}条结果:{}'.format(self.solution.result_count, ' '*93)

        self.tips['text'] = 'Tips: 搜索完成...'         # 更新主页面状态
        self.master.update()

    def search(self):
        if self.solution.try_connect_ftp(self.adds.adds, self.adds.sharedir):
            search_model = self.var.get()
            file_keyword = self.entry1.get().strip()
            dir_keyword = self.entry2.get().strip()
            dest = []

            if search_model in (0, 1):
                try:
                    dest = self.solution.search_fileANDdir(file_keyword, dir_keyword)
                except:
                    return []
            elif search_model == 2:
                try:
                    dest = self.solution.search_file(file_keyword)
                except:
                    return []
            elif search_model == 3:
                try:
                    dest = self.solution.search_dir(dir_keyword)
                except:
                    return []

            return dest
        else:
            return


class MyMenu():
    def __init__(self, win):
        self.create_filemenu(win)
        self.create_resetmenu(win)
        self.create_helpmenu(win)

    def create_filemenu(self, win):
        self.filemenu = tk.Menu(win.menubar, tearoff=0)
        self.filemenu.add_command(label='打开...                   Ctrl+O', command=win.openfile)
        self.filemenu.add_command(label='另存为...            Ctrl+Shift+S', command=win.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit                      Ctrl+Q', command=win.master.destroy)
        win.menubar.add_cascade(label='文件(F)', menu=self.filemenu)

    def create_helpmenu(self, win):
        self.helpmenu = tk.Menu(win.master, tearoff=0)
        self.helpmenu.add_command(label='关于            Ctrl+A', command=self.about)
        self.helpmenu.add_command(label='帮助             F1', command=win.open_help)
        win.menubar.add_cascade(label='帮助(H)', menu=self.helpmenu)

    def create_resetmenu(self, win):
        self.setmenu = tk.Menu(win.menubar, tearoff=0)
        self.setmenu.add_command(label='重设服务器地址   Ctrl+R', command=win.create_reset_adds)
        self.setmenu.add_command(label='重设共享文件夹   Ctrl+Y', command=win.create_reset_sharedir)
        win.menubar.add_cascade(label='设置(S)', menu=self.setmenu)

    def about(self):
        messagebox.showinfo('About', ' Create in Python3.7 by jw.zhang \n\n Email: xdzhangjingwen@163.com')

    def hello(self):
        pass


class Address():
    def __init__(self):
        self.adds = 'D:\\\\'
        self.sharedir = ''

    def change_adds(self, new_adds):
        self.adds = self.trans_path(new_adds)
        # regex = re.compile(r'\\\\\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        # try:
        #     self.adds = regex.fullmatch(new_adds).string
        # except Exception:
        #     self.adds = '非法地址，请核对！'

    def change_sharedir(self, new_dir):
        self.sharedir = self.trans_path(new_dir)

    def trans_path(self, path: str):
        result = []
        if path:
            for x in path:
                if x == '\\':
                    x = '\\\\'
                    result.append(x)
                else:
                    result.append(x)
        return ''.join(result)


class Window():
    def __init__(self):
        global root
        root = tk.Tk()
        root.title('文件资料快捷查询助手')
        self.win = [390, 145]
        self.width = int((root.winfo_screenwidth() - self.win[0]) / 2)
        self.height = int((root.winfo_screenheight() - self.win[1]) / 2)
        root.geometry('{}x{}+{}+{}'.format(self.win[0], self.win[1], self.width, self.height))
        root.resizable(False, False)


Window()
app = Application(master=root)
app.add_menu(MyMenu)
app.mainloop()
