from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import os

class HeaderRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, maxBytes, backupCount, *args, **kwargs):
        super(HeaderRotatingFileHandler, self).__init__(
            filename, *args, maxBytes=maxBytes, backupCount=backupCount,
             **kwargs
        )
        self._header = "######################## This Is Header ########################\n"
        self.addHeader(f"Log path : {__file__}")

    def doRollover(self):
        super(HeaderRotatingFileHandler, self).doRollover()
        if self._header != "":
            with open(self.baseFilename, 'a') as new_file:
                new_file.write(f"{self._header}")

    def setHeader(self, header):
        self._header = header

    def addHeader(self, header):
        self._header = f"{self._header}{header}'\n'"
        
        
class logging_class:
    MAX_LOG_FILES = 10
    MAX_LOG_SIZE_MB = 10
    
    def __init__(
        self,
        log_path = None,
        log_level_stream='INFO',
        log_name = None,
        verbose = False,
    ):
        self.log_name = log_name
        self.log_path = self.__default_log_pather(log_path,log_name)
        self.log_stream = verbose
        self.log_level_stream = log_level_stream
        self.formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d | %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s")
        self.header = ""

    def init_logger(self, stream=False):
        self.logger = logging.getLogger(self.log_name)
        if not self.logger.handlers:  
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False
            self.add_file_handler('INFO')

            init_handler = self.__handler_list_maker(
                level=self.log_level_stream,
                stream=stream, 
                file=True,
            )
            for _handler in init_handler:
                self.logger.addHandler(_handler)
        return self.logger

    def __handler_list_maker(self,level, stream=False, file=True):
        _level = self.__log_level_converter(level)
        handler_list = []
        if stream:
            stream_handler.setFormatter(self.formatter)
            stream_handler.setLevel(_level)
            handler_list.append(stream_handler)
        if file:
            filename = f'{self.log_path}/{self.log_name}_{level}.log'
            Path(f'{self.log_path}').mkdir(parents=True, exist_ok=True)  
            maxBytes = 1024 * 1024 * logging_class.MAX_LOG_SIZE_MB
            backupCount = logging_class.MAX_LOG_FILES
            
            file_handler = HeaderRotatingFileHandler(
                filename = filename,
                maxBytes = maxBytes, 
                backupCount = backupCount)
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(_level)
            handler_list.append(file_handler)
        return handler_list


    def add_file_handler(self, level):
        filename = f'{self.log_path}/{self.log_name}_{level}.log'
        Path(self.log_path).mkdir(parents=True, exist_ok=True)  
        maxBytes = 1024 * 1024 * self.MAX_LOG_SIZE_MB
        backupCount = self.MAX_LOG_FILES
        
        file_handler = HeaderRotatingFileHandler(filename=filename, maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(getattr(logging, level.upper()))
        
        self.logger.addHandler(file_handler)

    
    def add_header_handlers(self, header):
        for __handler in self.logger.handlers:
            if __handler.__class__.__name__ == 'HeaderRotatingFileHandler':
                __handler.addHeader(header)
        

    def __log_namer(self, log_name):
        if log_name is None:
            return f"{os.path.basename(__file__)}"
        else:

            return log_name

    def __log_level_converter(self, level):
        _level = str(level).upper()
        if _level == 'DEBUG':
            return logging.DEBUG
        elif _level == 'INFO':
            return logging.INFO
        elif _level == 'WARNING':
            return logging.WARNING
        elif _level == 'ERROR':
            return logging.ERROR
        elif _level == 'CRITICAL':
            return logging.CRITICgeonAL
        else:
            assert False, f'Check level {_level}'

    def __default_log_pather(self, log_path, log_name):
        final_path = Path(log_path) / log_name
        final_path.mkdir(parents=True, exist_ok=True)
        return str(final_path)


    def add_logger(self,log_path, log_name, log_level='INFO', stream=False):
            log_module = logging_class(
                log_path = log_path,
                log_level_stream='INFO',
                log_name = log_name)
            
            log_module.init_logger(stream=stream)
            if log_level.upper() != 'INFO':
                log_module.add_file_handler(level=log_level.upper())
            return log_module


def setup_logger(ini_dict):
    log_path = ini_dict['CONFIG']['LOG_FILE_PATH']
    log_name = ini_dict['CONFIG']['LOG_FILE_NAME']
    log_level = ini_dict['CONFIG']['LOG_LEVEL'].upper()

    logger_instance = logging_class(
        log_path=log_path,
        log_level_stream=log_level,
        log_name=log_name
    )
    logger_instance.init_logger(stream=False)
    return logger_instance.logger