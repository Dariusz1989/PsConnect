#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月7日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: Test
@description: 
"""
import os

from Constant import CodeOpenImage, CodeGetImage
from Protocol import Protocol
from PsConnect import PsConnect


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"

if __name__ == '__main__':
    # debug
    Protocol.DEBUG = True

    PsConnect.connect('127.0.0.1', 49494, '123456')
    # 获取ps版本
    msg = PsConnect.send('app.version;')
    print('******', msg, msg.data)

    # 打开图片
    msg = PsConnect.send(CodeOpenImage.format(
        os.path.abspath('images/head.jpg').replace('\\', '/')))
    result = msg.toDict()
    print('******', msg, msg.data, result)

    # 获取图片
    msg = PsConnect.send(CodeGetImage.format(
        result.id, result.width, result.height))
    print('******', msg, msg.isImg())

    try:
        import sys
        from PyQt5.QtWidgets import QApplication, QLabel
        from PyQt5.QtGui import QPixmap
        app = QApplication(sys.argv)
        w = QLabel()
        w.setScaledContents(True)
        w.resize(result.width, result.height)
        pixmap = QPixmap()
        # open('out.jpg', 'wb').write(msg.data)
        pixmap.loadFromData(msg.data)
        w.setPixmap(pixmap)
        w.show()
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except:
        input('Press any key to exit')
