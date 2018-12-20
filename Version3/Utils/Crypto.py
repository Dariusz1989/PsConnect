#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月7日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: Crypto
@description: 
"""
from hashlib import pbkdf2_hmac
import sys

from Cryptodome.Cipher import DES3


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


PYTHON_MAJOR_VERSION = sys.version_info[0]


class Crypto:
    # 加解密工具类

    SALT = b'Adobe Photoshop'
    ITERACTIONCOUNT = 1000
    KEY_LENGTH = 24

    def __init__(self, password):
        self._key = pbkdf2_hmac(
            'sha1', password.encode(), self.SALT, self.ITERACTIONCOUNT, self.KEY_LENGTH)
        self._iv = b'\0\0\0\0\0\0\0\0'
        self.block_size = 8

    def encrypt(self, b):
        data = self._padData(b)
        return DES3.new(self._key, DES3.MODE_CBC, self._iv).encrypt(data)

    def decrypt(self, byteString):
        data = DES3.new(self._key, DES3.MODE_CBC, self._iv).decrypt(byteString)
        return self._unpadData(data)

    # PKCS5 padding
    def _padData(self, data):
        pad_len = 8 - (len(data) % self.block_size)
        if PYTHON_MAJOR_VERSION < 3:
            data += pad_len * chr(pad_len)
        else:
            data += bytes([pad_len] * pad_len)

        return data

    def _unpadData(self, data):
        # Unpad data depending on the mode.
        if not data:
            return data

        if PYTHON_MAJOR_VERSION < 3:
            pad_len = ord(data[-1])
        else:
            pad_len = data[-1]
        data = data[:-pad_len]

        return data