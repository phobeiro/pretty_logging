import logging
import pandas as pd

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
