#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年12月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.TcpSocket
@description: 
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QTcpSocket


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class TcpSocket(QTcpSocket):

    # 连接被关闭断开时发出
    connectClosed = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(TcpSocket, self).__init__(*args, **kwargs)
        # 连接成功的信号
        self.connected.connect(self.onRemoteConnected)
        # 连接丢失信号
        self.disconnected.connect(self.onRemoteDisconnected)
        # 准备读取信号
        self.readyRead.connect(self.onRemoteReadyRead)
        # 连接错误信号
        self.error.connect(self.onRemoteError)

    def onRemoteConnected(self):
        print('连接成功')

    def onRemoteDisconnected(self):
        print('断开连接')
        self.connectClosed.emit('断开连接')

    def onRemoteReadyRead(self):
        # 读取接收的数据
        if self.bytesAvailable():
            data = self.readAll()
            print('接收到数据: ', type(data), data.data())

    def onRemoteError(self, socketError):
        if socketError == self.ConnectionRefusedError:
            print('连接被对等方拒绝(或超时)')
            self.connectClosed.emit('连接被对等方拒绝(或超时)')
        elif socketError == self.RemoteHostClosedError:
            print('远程连接被关闭')
            self.connectClosed.emit('远程连接被关闭')
        elif socketError == self.HostNotFoundError:
            print('找不到主机地址')
            self.connectClosed.emit('找不到主机地址')
        elif socketError == self.SocketTimeoutError:
            print('套接字操作超时')
            self.connectClosed.emit('套接字操作超时')
        elif socketError == self.NetworkError:
            print('网络发生错误(例如: 网络电缆被意外拔出)')
            self.connectClosed.emit('网络发生错误(例如: 网络电缆被意外拔出)')
        else:
            print('其他错误:', self.errorString())
