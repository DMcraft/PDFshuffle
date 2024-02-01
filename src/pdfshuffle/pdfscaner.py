#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 07/01/2024
# version ='1.0'
# Copyright 2024 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------
# pyuic5 scanerwindow.ui -o scanerwindow.py

""" Вспомогательная программа сканирования изображений.

"""

from loguru import logger
from os import environ
import scaner


if __name__ == '__main__':
    if environ.get('PRODUCTION') is None:
        logger.remove(handler_id=None)
        logger.add("runtime.log", rotation="10 MB")

    scaner.main()
