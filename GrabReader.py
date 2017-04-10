# coding: utf-8
import random
import time
import numpy as np
import ctypes
import win32gui
import win32api
import win32con
from PIL import ImageGrab

from FlappyBirdPlayer import FlappyBirdPlayer as Player

class RECT(ctypes.Structure): 
    _fields_ = [('left', ctypes.c_long), 
            ('top', ctypes.c_long), 
            ('right', ctypes.c_long), 
            ('bottom', ctypes.c_long)] 
    def __str__(self): 
        return str((self.left, self.top, self.right, self.bottom)) 


c = 0

class GrabReader:

    def __init__(self, label): 
        self.label = label

        hld = win32gui.FindWindow(None, label)

        win32gui.ShowWindow(hld, win32con.SW_RESTORE)  # 强行显示界面后才好截图
      # win32gui.SetForegroundWindow(hld)  # 将窗口提到最前

        # 取当前窗口坐标  
        rect = RECT() 
        ctypes.windll.user32.GetWindowRect(hld,ctypes.byref(rect)) 
        self.hld = hld

        # 调整坐标  
        self.rangle = (rect.left+2,rect.top+22,rect.right-2,rect.bottom-20) 
        self.first = None
        self.second = ImageGrab.grab(self.rangle)
        self.third = ImageGrab.grab(self.rangle)

        self.player = Player()

    def state(self, action):
        # 抓图
        global c
        if action[1] == 1:
            self.act()
        else:
            time.sleep(0.02)

        self.first = self.second
        pic = ImageGrab.grab(self.rangle)
        self.second = pic

        reward, terminal = self.player.checkTerminal(np.asarray(self.second))
        if terminal:
            self.second.save(str(c) + '.jpg')
            c += 1
            self.player.wait_restart(self.first, self.second, self.rangle)
            self.act()

        img_data = np.asarray(self.second)
        return img_data, reward, terminal

    def act(self):
        self.player.act(self.hld)

