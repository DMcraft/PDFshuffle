#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 04/10/2023
# version ='2.4.1'
# Copyright 2023 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------

""" A program for easy and visual recombination of sheets of PDF files,
as well as adding sheets of images from files and scanner.

Программа для легкой и наглядной перекомбинации листов PDF файлов,
а также добавления листов изображений из файлов и сканера.

"""

from loguru import logger
from os import environ
import shuffle

# import sys
# from PyQt5.QtGui import QPixmap
#
# # Добавьте в начало main.py
# sys.modules['PyQt5.QtGui'].QPixmap.__reduce__ = lambda self: (QPixmap, (None,))

import sys
import traceback
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.critical(f"Unhandled exception:\n{tb}")
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

if __name__ == '__main__':
    if environ.get('PRODUCTION') is None:
        logger.remove(handler_id=None)
        logger.add("pdfshuffle.log", rotation="10 MB")

    print('Start program...')

    shuffle.main()

    print('Stop program.')
