import logging
from time import sleep

from app.parser import Parser

def run():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    from app.client import Client
    data = {'phone': '1111111'}
    Client.send(data=data)

    # parser = Parser()
    #
    # while True:
    #     parser.parse()
    #     sleep(60)
