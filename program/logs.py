import logging
from logging.handlers import RotatingFileHandler

class Log:
    FORMAT = '%(asctime)s %(levelname)s(%(funcName)s): %(message)s'
    handler = RotatingFileHandler(
        'log/Log.log', maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(FORMAT))
     
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    
    def __init__(self):
        return None
        

if __name__ == '__main__':
    
    pass
    