#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import glob
import os
import sys

import PyQt5
import py2exe  # @UnusedImport


# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0
sys.path.append('../')

# windows 无控制台
# console  有控制台


sys.argv.append('py2exe')  # 允许程序通过双击的形式执行

includes = [
    'sip',
    'PyQt5.QtCore',
    'PyQt5.QtWidgets',
    'PyQt5.QtGui',
    'PyQt5.QtNetwork',
    'PyQt5.QtPrintSupport',
    'PyQt5.QtSvg'
]

excludes = [
    'cffi'
]

qtpath = os.path.dirname(PyQt5.__file__)
dll_excludes = ['MSVCP90.dll', 'MSVCR90.dll',
                'MSVCP100.dll', 'MSVCR100.dll', 'w9xpopen.exe']

# compressed 为1 则压缩文件
# optimize 为优化级别 默认为0
options = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 2,
        'includes': includes,
        'excludes': excludes,
        'dll_excludes': dll_excludes
    }
}

setup(
    version='1.0',
    description='PsConnect',
    name='PsConnect',
    zipfile=None,
    options=options,
    windows=[{
        'script': 'FrameworkTools.py',
                'icon_resources': [(1, 'images/app.ico')],
    }],
    data_files=[
        ('', ['qt.conf', 'Cryptodome/Cipher/_raw_cbc{}.pyd'.format(
            '.cp35-win32' if sys.version_info[1] > 4 else ''),
            'Cryptodome/Cipher/_raw_des3{}.pyd'.format('.cp35-win32' if sys.version_info[1] > 4 else '')]),
        ('images', ['images/app.ico']),
        ('plugins/platforms',
         glob.glob(qtpath + '/plugins/platforms/*.dll')),
        ('plugins/iconengines',
         glob.glob(qtpath + '/plugins/iconengines/*.dll')),
        ('plugins/imageformats',
         glob.glob(qtpath + '/plugins/imageformats/*.dll')),
        ('plugins/printsupport',
         glob.glob(qtpath + '/plugins/printsupport/*.dll')),
    ]
)

# D:\soft\Python34\python setup.py py2exe
