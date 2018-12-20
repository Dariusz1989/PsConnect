#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月29日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: FrameworkTools
@description: 
"""
import base64
import struct


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


_DELTA = 0x9E3779B9


def _long2str(v, w):
    n = (len(v) - 1) << 2
    if w:
        m = v[-1]
        if (m < n - 3) or (m > n):
            return ''
        n = m
    s = struct.pack('<%iL' % len(v), *v)
    return s[0:n] if w else s


def _str2long(s, w):
    if not isinstance(s, bytes):
        s = str(s).encode()
    n = len(s)
    m = (4 - (n & 3) & 3) + n
    s = s.ljust(m, b'\0')
    v = list(struct.unpack(('<%iL' % (m >> 2)).encode(), s))
    if w:
        v.append(n)
    return v


def encrypt(strs, key):
    if strs == '':
        return strs
    v = _str2long(strs, True)
    k = _str2long(key.ljust(16, "\0"), False)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    sums = 0
    q = 6 + 52 // (n + 1)
    while q > 0:
        sums = (sums + _DELTA) & 0xffffffff
        e = sums >> 2 & 3
        for p in range(n):
            y = v[p + 1]
            v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                            ^ (sums ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
            z = v[p]
        y = v[0]
        v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                        ^ (sums ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff
        z = v[n]
        q -= 1
    return _long2str(v, False)


def decrypt(strs, key):
    if strs == '':
        return strs
    v = _str2long(strs, False)
    k = _str2long(key.ljust(16, '\0'), False)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    q = 6 + 52 // (n + 1)
    sums = (q * _DELTA) & 0xffffffff
    while (sums != 0):
        e = sums >> 2 & 3
        for p in range(n, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                            ^ (sums ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
            y = v[p]
        z = v[n]
        v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                        ^ (sums ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
        y = v[0]
        sums = (sums - _DELTA) & 0xffffffff
    return _long2str(v, True)


def encryptToBase64(data, key):
    return base64.b64encode(encrypt(data, key)).decode()


def decryptFromBase64(data, key):
    return decrypt(base64.b64decode(data), key).decode()


if __name__ == '__main__':
    key = '0123456789abcdef'
    data = '哈哈'

    s = encrypt(data, key)
    print(s)
    print(base64.b64encode(s))

    s = decrypt(s, key)
    print(s.decode())

    s = encryptToBase64(data, key)
    print(s)
    s = decryptFromBase64(s, key)
    print(s)
