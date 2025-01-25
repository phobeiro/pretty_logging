from config import config

import logging
from pathlib import Path
from typing import Literal

import pandas as pd


c = config.Config

class LineByLineFileHandler(logging.FileHandler):
    def emit(self, record):
        msg = self.format(record)
        if isinstance(record.msg, pd.DataFrame):
            record.msg = record.msg.to_string()

        if isinstance(record.msg, str):
            for line in record.msg.splitlines():
                new_record = logging.LogRecord(
                    record.name, record.levelno, record.pathname, record.lineno,
                    line, record.args, record.exc_info, record.funcName
                )
                msg = self.format(new_record)
                
                super().emit(new_record)
        else:
            super().emit(record)


class LineByLineStreamFileHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        if isinstance(record.msg, pd.DataFrame):
            record.msg = record.msg.to_string()

        if isinstance(record.msg, str) or isinstance(record.msg, str):
            for line in record.msg.splitlines():
                new_record = logging.LogRecord(
                    record.name, record.levelno, record.pathname, record.lineno,
                    line, record.args, record.exc_info, record.funcName
                )
                msg = self.format(new_record)
                
                super().emit(new_record)
        else:
            super().emit(record)

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
        f_handler = LineByLineFileHandler(file_path)
        f_handler.terminator = terminator
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(formater)
        logger.addHandler(f_handler)

    if (handler == 'stream') or (handler == 'both'):
        # stream logging config
        s_handler = LineByLineStreamFileHandler()
        s_handler.terminator = terminator
        s_handler.setLevel(logging.INFO)
        s_handler.setFormatter(formater)
        logger.addHandler(s_handler)

    return logger
