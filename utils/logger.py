import time
from pathlib import Path
from loguru import logger
from django.conf import settings

log_path = Path(settings.LOG_PATH)

def getLogger(name):
    log_path_info = log_path.joinpath(f'{name}_{time.strftime("%Y-%m-%d")}.log')
    # 日志简单配置 文件区分不同级别的日志
    logger.add(log_path_info,
              rotation=settings.LOGGER.get('maxBytes'),
              encoding='utf-8',
              enqueue=True,
              level=settings.LOGGER.get('level'),
              retention=settings.LOGGER.get('retention'),
              compression=settings.LOGGER.get('compression'))

    return logger
