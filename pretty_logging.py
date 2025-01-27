from config import config
from handlers import linebylinefilehandler, linebylinestreamhandler

import logging
from pathlib import Path
from typing import Literal

c = config.Config

def pretty_logging(
        logger_name:str, 
        handler:Literal['stream', 'file', 'both'] = 'stream') -> logging.Logger:
    '''
    Create INFO logging messages with line breaking for strings and DataFrames.
    logger_name: name for the logger
    handler: "stream", "file", "both". Default: "stream"
    '''
    
    logger = logging.getLogger(logger_name)
    logger.propagate = False

    # logging config
    fmt = c.LOG_FMT
    datefmt = c.LOG_DATEFMT
    terminator = c.LOG_TERMINATOR
    formater = logging.Formatter(fmt=fmt, datefmt=datefmt)

    if (handler == 'file') or (handler == 'both'):
        # file logging config
        file_path = Path(c.FILE_PATH)
        f_handler = linebylinefilehandler.LineByLineFileHandler(file_path)
        f_handler.terminator = terminator
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(formater)
        logger.addHandler(f_handler)

    if (handler == 'stream') or (handler == 'both'):
        # stream logging config
        s_handler = linebylinestreamhandler.LineByLineStreamHandler()
        s_handler.terminator = terminator
        s_handler.setLevel(logging.INFO)
        s_handler.setFormatter(formater)
        logger.addHandler(s_handler)

    return logger
