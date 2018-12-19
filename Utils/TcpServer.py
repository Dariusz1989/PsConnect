#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年12月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.TcpServer
@description: 
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QTcpServer


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class TcpServer(QTcpServer):

    # 接收到消息的信号
    messageReceived = pyqtSignal(bytes)

    def __init__(self, *args, **kwargs):
        super(TcpServer, self).__init__(*args, **kwargs)
        self.newConnection.connect(self.onNewConnection)

    def onNewConnection(self):
        # 当有新的连接来时
        while self.hasPendingConnections():
            socket = self.nextPendingConnection()
            socket.readyRead.connect(self.onReadyRead)
            if socket.bytesAvailable() > 0:
                # 如果已有数据发送过来
                self.doRecv(socket)

    def onReadyRead(self):
        # 准备接收数据
        socket = self.sender()
        if socket.bytesAvailable() > 0:
            self.doRecv(socket)

    def doRecv(self, socket):
        # 接收数据
        try:
            data = socket.readAll().data()
            self.messageReceived.emit(data)
        except Exception as e:
            self.messageReceived.emit(str(e).encode())
