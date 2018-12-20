#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月7日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: Protocol
@description: 
"""
import binascii
import struct

from Utils.Crypto import Crypto


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Message:

    def __init__(self, tid, ctype, data, status=0):
        '''
        :param tid:    传输id
        :param ctype:  内容类型
        :param data:   内容
        :param status: 状态
        '''
        self.tid = tid
        self.ctype = ctype
        self.data = data
        self.status = status

    def isImg(self):
        return self.ctype == 3

    def isText(self):
        return self.ctype == 2

    def __str__(self):
        return '[status: {}, tid: {}, type: {}, isText: {}, isImage: {}, data len: {}]'.format(
            self.status, self.tid, self.ctype, self.isText(), self.isImg(), len(self.data))


class Protocol:

    DEBUG = 0                         # 是否显示调试内容
    TRANSACTIONID = 0                 # 传输id
    PROTOCOL_VERSION = 1              # 协议版本
    PROTOCOL_LENGTH = 12              # 协议长度
    COMM_LENGTH = 4                   # comm长度
    NO_COMM_ERROR = 0                 # 没有错误
    COMM_ERROR = 1                    # 错误

    # Content Type  内容类型
    ILLEGAL_TYPE = 0
    ERRORSTRING_TYPE = 1              # 错误字符
    JAVASCRIPT_TYPE = 2               # javascript代码
    IMAGE_TYPE = 3                    # 图像
    PROFILE_TYPE = 4                  # ICC profile
    DATA_TYPE = 5                     # 任意的数据

    @classmethod
    def init(cls, password):
        cls.TRANSACTIONID = 0
        cls._crypt = Crypto(str(password).strip())

    @classmethod
    def increase(cls):
        # 传输id自增
        cls.TRANSACTIONID += 1

    @classmethod
    def pack(cls, content, ctype=2):
        """
        Unencrypted:                         不加密
            4 bytes Length of message            4字节的内容长度
            4 bytes Communication Status         4字节的状态码
        Encrypted:                           加密
            4 bytes Protocol Version             4字节协议版本
            4 bytes Transaction ID               4字节传输ID
            4 bytes Content Type                 4字节内容类型
            n bytes Content                      n字节的内容

        :param content: 待封包数据
        :param ctype:   Content Type类型
        :return: 返回加密内容
        """
        if not isinstance(content, bytes):
            # 必须是bytes类型
            content = str(content).encode()

        # 先对数据进行封装并加密[4协议版本 + 4传输id + 4类型 + 内容]
        body = struct.pack('>iii{}s'.format(
            len(content)), cls.PROTOCOL_VERSION,
            cls.TRANSACTIONID, ctype, content) + b'\n'
        if cls.DEBUG:
            print('Protocol Version:    ', cls.PROTOCOL_VERSION)
            print('Transaction ID:      ', cls.TRANSACTIONID)
            print('Content Type:        ', ctype)
            print('Content:             ',
                  content[:10] + b'......' + content[-10:])
            print('Body:                ', body[:10] + b'......' + body[-10:])
            hbody = binascii.hexlify(body)
            print('Hexlify:             ',
                  hbody[:10] + b'......' + hbody[-10:])

        # 对数据加密
        enBody = cls._crypt.encrypt(body)
        if cls.DEBUG:
            print('EnBody:              ',
                  enBody[:10] + b'......' + enBody[-10:])
            henBody = binascii.hexlify(enBody)
            print('Hexlify:             ',
                  henBody[:10] + b'......' + henBody[-10:])

        # 封装头部[4长度 + 4状态 + 内容1]
        mLength = cls.COMM_LENGTH + len(enBody)  # 状态码长度+内容长度
        allBytes = struct.pack('>i', mLength) + \
            struct.pack('>i', cls.NO_COMM_ERROR) + enBody

        if cls.DEBUG:
            print('Length of message:   ', mLength)
            print('Communication Status:', cls.NO_COMM_ERROR)
            print('AllBytes:            ',
                  allBytes[:10] + b'......' + allBytes[-10:])
            hallBytes = binascii.hexlify(allBytes)
            print('Hexlify:             ',
                  hallBytes[:10] + b'......' + hallBytes[-10:])
        return allBytes

    @classmethod
    def unpack(cls, rawContent):
        """
        Unencrypted:                         无加密
            4 bytes Length of message            4字节的内容长度
            4 bytes Communication Status         4字节的状态码
        Encrypted:                           加密
            4 bytes Protocol Version             4字节协议版本
            4 bytes Transaction ID               4字节传输ID
            4 bytes Content Type                 4字节内容类型
            n bytes Content                      n字节的内容

        :param rawContent: 待解包数据
        """
        if not rawContent:
            return Message(cls.TRANSACTIONID, cls.ERRORSTRING_TYPE, b'')
        # 解包整体[4消息长度 + 4状态 + 消息]
        mLength, status, content = struct.unpack(
            '>ii{}s'.format(len(rawContent) - 8), rawContent)
        if cls.DEBUG:
            print('Reading length:      ', mLength)
            print('Reading com status:  ', status)
            print('Read en message:     ',
                  content[:10] + b'......' + content[-10:])

        if status == 0:  # 只有没有错误时才会对数据解密,否则返回的是原始数据
            content = cls._crypt.decrypt(content)

        if cls.DEBUG:
            print('Read de message:     ',
                  content[:10] + b'......' + content[-10:])
            hcontent = binascii.hexlify(content)
            print('Hexlify:             ',
                  hcontent[:10] + b'......' + hcontent[-10:])
        # 对解密的数据解包[4协议版本 + 4传输id + 4类型 + 内容]
        version, transactionid, ctype, content = struct.unpack(
            '>iii{}s'.format(len(content) - cls.PROTOCOL_LENGTH), content)
        if ctype == cls.IMAGE_TYPE:
            # 如果是图片需要去掉头部1字节的类型 ==1表示jpg ==2表示pixmap
            content = content[1:]
        if cls.DEBUG:
            print('Protocol Version:    ', version)
            print('Transaction ID:      ', transactionid)
            print('Content Type:        ', ctype)
            print('Content:             ',
                  content[:10] + b'......' + content[-10:])

        return Message(transactionid, ctype, content, status)
