#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 04/10/2023
# version ='2.10'
# Copyright 2023 Dmitriy Aldunin
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------------------

"""Программа для легкой и наглядной перекомбинации листов PDF файлов,
а также добавления листов изображений из файлов и сканера."""
import sys
import os
from loguru import logger
from shuffle import main as shuffle_main

if __name__ == '__main__':
    logger.remove()
    if os.getenv('PRODUCTION') is None:
        logger.add("pdfshuffle.log", level="INFO", rotation="10 MB")
    else:
        logger.add(sys.stderr, level="DEBUG")

    print('Запуск программы...')

    try:
        shuffle_main()
    except Exception as e:
        logger.error(f"Произошла ошибка при выполнении программы: {e}")
        print(f"Ошибка: {e}")

    print('Программа завершена.')