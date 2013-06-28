import logging
from logging import handlers

def getLogger(app):
    logger = logging.getLogger(app)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    #fh = logging.FileHandler(config.get("path","log_file"))
    fh = handlers.TimedRotatingFileHandler(os.path.join(os.environ["HOME"], "local/geoserver_wrapper/logs/geoserver_wrapper.log"), when='midnight')
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    return logger

