#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年2月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Client
@description: 
"""
import cgitb
import os
import sys

from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QApplication

from FrameworkTools import Window


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

if __name__ == '__main__':
    sys.excepthook = cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    app.setApplicationName('PS连接测试工具')
    app.setApplicationDisplayName('PS连接测试工具')
    app.setApplicationVersion('1.0')
    app.setStyle('Fusion')
    if os.path.exists('images/app.ico'):
        app.setWindowIcon(QIcon('images/app.ico'))
    w = Window()
    w.show()
    sys.exit(app.exec_())