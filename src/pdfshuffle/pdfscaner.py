#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 15/11/2024
# version ='2.10'
# Copyright 2024 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------

""" Вспомогательная программа сканирования изображений.

"""
import logging
import sys

from loguru import logger
from os import environ
import scaner

if __name__ == '__main__':
    if environ.get('PRODUCTION') is None:
        logger.remove(handler_id=None)
        logger.add("pdfshuffle.log", level="INFO", rotation="10 MB")
    else:
        logger.remove(handler_id=None)
        logger.add(sys.stderr, level="DEBUG")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    scaner.SCANER_START_MAIN = True
    scaner.main()
