import logging
from pythonjsonlogger import jsonlogger

def get_logger(name: str, level=logging.INFO):
  logger = logging.getLogger(name)
  logger.setLevel(level)

  formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z',
    json_ensure_ascii=False,
  )

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)

  logger.addHandler(stream_handler)

  return logger
