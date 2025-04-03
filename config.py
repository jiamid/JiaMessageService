from functools import lru_cache
import json
from loguru import logger


@lru_cache()
def get_config():
    with open('config.json','r',encoding='utf-8') as f:
        data = json.load(f)
    logger.info(f'LoadConfig:{data}')
    return data

if __name__ == '__main__':
    print(get_config())
    print(get_config())
    print(get_config())
