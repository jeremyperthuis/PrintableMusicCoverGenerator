import logging
import configparser
from src.Interface import *

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s  %(levelname)s : %(funcName)s  %(message)s', level=logging.INFO)

    path = os.path.dirname(os.path.abspath("."))
    config = configparser.ConfigParser()
    config.read(os.path.join(path,"themes\\default.ini"))

    g=Interface()