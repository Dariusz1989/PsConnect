import os

from Cryptodome.Cipher._mode_cbc import _create_cbc_cipher


def _create_cipher(factory, key, mode, *args, **kwargs):

    kwargs["key"] = key

    if args:
        if mode in (2, 3, 5, 7):
            if len(args) > 1:
                raise TypeError("Too many arguments for this mode")
            kwargs["IV"] = args[0]

    return _create_cbc_cipher(factory, **kwargs)
