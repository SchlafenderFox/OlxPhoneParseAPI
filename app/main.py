import logging
from time import sleep

from app.parser import Parser

def run():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    parser = Parser()

    while True:
        parser.parse()
        sleep(60)
