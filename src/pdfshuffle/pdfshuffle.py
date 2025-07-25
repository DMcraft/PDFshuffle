#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 04/10/2023
# version ='2.9'
# Copyright 2023 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------

""" A program for easy and visual recombination of sheets of PDF files,
as well as adding sheets of images from files and scanner.

Программа для легкой и наглядной перекомбинации листов PDF файлов,
а также добавления листов изображений из файлов и сканера.

"""
import sys

from loguru import logger
import logging
from os import environ
import shuffle

if __name__ == '__main__':
    if environ.get('PRODUCTION') is None:
        logger.remove(handler_id=None)
        logger.add("pdfshuffle.log", level="INFO", rotation="10 MB")
    else:
        logger.remove(handler_id=None)
        logger.add(sys.stderr, level="DEBUG")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    print('Start program...')

    shuffle.main()

    print('Stop program.')
