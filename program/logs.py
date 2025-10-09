import logging

class Log:
    FORMAT = '%(asctime)s %(levelname)s(%(funcName)s): %(message)s'
    logging.basicConfig(level=logging.DEBUG, 
                        filename='C:/VsCode/build/fatigue/log/Log.log', 
                        filemode='w', 
                        format=FORMAT, 
                        encoding='utf-8')
    logger = logging.getLogger()
    
    def __init__(self):
        return None
        
        

if __name__ == '__main__':
    log = Log()
    log.logger.info('This is an info message')
    log.logger.warning('This is a debug message')