#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 04/10/2023
# version ='2.1'
# Copyright 2023 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------

""" A program for easy and visual recombination of sheets of PDF files,
as well as adding sheets of images from files and scanner.

Программа для легкой и наглядной перекомбинации листов PDF файлов,
а также добавления листов изображений из файлов и сканера.

"""

from loguru import logger
import shuffle

PRODUCTION = False

if __name__ == '__main__':
    if PRODUCTION:
        logger.remove(handler_id=None)
        logger.add("runtime.log", rotation="10 MB")

    print('Start program...')

    shuffle.main()

    print('Stop program.')
