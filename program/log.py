import logging

class Log:
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, 
                        filename='C:/VsCode/build/fatigue/log/Log.log', 
                        filemode='w', 
                        format=FORMAT)
    logger = logging.getLogger()
        
        

if __name__ == '__main__':
    log = Log()
    log.logger.info('This is an info message')
    log.logger.debug('This is a debug message')