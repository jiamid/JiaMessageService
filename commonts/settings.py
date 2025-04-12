# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 17:29
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : settings.py
# @Software: PyCharm
from pydantic_settings import BaseSettings, SettingsConfigDict
import base64


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.prod.env', '.dev.env'),  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8')

    debug: bool = True
    port: int = 9998
    db_name: str = 'message_db'
    bot_token: str = 'ODEwMTk5MjQ5NzpBQUhWWXZhMFRhR180Q3Y3cWtYdko1NXBpZkRaWEp5aXpZWQ=='
    worker_chat_id: str = 'all'
    worker_api_pre: str = 'http://43.160.195.19'

    def get_bot_token(self):
        return base64.b64decode(self.bot_token.encode()).decode()


settings = Settings()
