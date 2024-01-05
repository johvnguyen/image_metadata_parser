from PNGParser.PNGParser import PNGParser
import os
import logging
import time

'test-' + time.strftime("%Y%m%d-%H%M%S")+ '.log'

logging.basicConfig(filename = f'logs/png_driver{time.strftime("%Y%m%d-%H%M%S")}.log', encoding = 'utf-8', level = logging.DEBUG)

if __name__ == '__main__':
    png_parser = PNGParser()
    png_parser.parse('images/modern-view-acrobat.png.img.png')
    png_parser.print_metadata()

    exit()