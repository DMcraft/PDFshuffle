#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 15/11/2024
# version ='2.5'
# Copyright 2024 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------

""" Вспомогательная программа сканирования изображений.

"""

from loguru import logger
from os import environ
import scaner


if __name__ == '__main__':
    if environ.get('PRODUCTION') is None:
        logger.remove(handler_id=None)
        logger.add("runtime.log", rotation="10 MB")
    scaner.SCANER_START_MAIN = True
    scaner.main()
