#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月7日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: PsConnect
@description: 
"""
import socket
import struct

from Protocol import Protocol


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class PsConnect:

    _socket = None

    @classmethod
    def connect(cls, host, port, pwd):
        """连接服务器
        :param cls:
        :param host: 地址
        :param port: 端口
        :param pwd: 密码
        """
        Protocol.init(pwd)
        cls._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls._socket.settimeout(10)  # 10s 超时
        try:
            cls._socket.connect((host, port))
        except Exception as e:
            cls._socket = None
            raise e

    @classmethod
    def send(cls, data, ctype=2, img=False):
        """发送数据
        :param cls:
        :param data:  数据
        :param ctype: 类型
        :param img:   表示本次接收的数据是否为图片
        """
        assert cls._socket != None
        cls._socket.sendall(Protocol.pack(data, ctype))
        Protocol.increase()
        return cls.recv(img)

    @classmethod
    def recv(cls, img=False):
        """接收数据
        :param img:   表示本次接收的数据是否为图片
        """
        assert cls._socket != None
        try:
            # 数据长度
            header = cls._socket.recv(4)
            totalSize, = struct.unpack('>i', header)
            recvSize = 0
            totalData = header
            while recvSize < totalSize:
                recvData = cls._socket.recv(1024)
                recvSize += len(recvData)
                totalData += recvData
            if img:
                # 获取图片的代码后面会有其它字符串(其实是两个包)
                try:  # 如果是超时则不管它
                    totalData += cls._socket.recv(1024)
                except:
                    pass
        except:
            totalData = None
        message = Protocol.unpack(totalData)
        return message
