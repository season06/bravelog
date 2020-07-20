import logging

# try except: exc_info=true

class Logger():
    def __init__(self, logger):
        # create a logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # define the output format
        LEVEL = logging.DEBUG
        FORMAT = '%(asctime)s , %(name)s , %(levelname)s: %(message)s'
        DATAFMT='%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(FORMAT, DATAFMT)

        # create a handler to write into the file
        file_handler = logging.FileHandler('log.txt')
        file_handler.setLevel(LEVEL)
        file_handler.setFormatter(formatter)

        # create a handler to print on the screen
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LEVEL)
        stream_handler.setFormatter(formatter)

        # add handler to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def debug(self, msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)
    
    def log(self, level, msg):
        self.logger.log(level, msg)
    
    def setLevel(self, level):
        self.logger.setLevel(level)
    
    def disable(self): # close log file
        logging.disable(50)