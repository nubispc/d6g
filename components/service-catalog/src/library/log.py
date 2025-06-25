import logging
from uvicorn.logging import DefaultFormatter

class LoggerFactory:
    _configured = False
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if not cls._configured:
            cls._setup_logging()
            cls._configured = True
        
        return logging.getLogger(name)
    
    @classmethod
    def _setup_logging(cls):
        # Configure root logger with uvicorn format
        handler = logging.StreamHandler()
        handler.setFormatter(DefaultFormatter("%(levelprefix)s [%(name)s] %(message)s"))
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.handlers.clear()
        root_logger.addHandler(handler)