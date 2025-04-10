# -*- coding: utf-8 -*-
# @Time    : 2024/7/26 17:12
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : bot.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, Dispatcher, Router
from loguru import logger
from commonts.settings import settings

bot = Bot(token=settings.get_bot_token())

telegram_router = Router(name="telegram")
dp = Dispatcher()
dp.include_router(telegram_router)


async def send_message_to_bot(chat_id: str, text: str, parse_mode=None):
    flag = True
    times = 1
    while flag and times < 3:
        try:
            await bot.send_message(chat_id, text=text, parse_mode=parse_mode)
            flag = False
        except Exception as e:
            logger.error(f'send message fail {times} e:{e}')
            times += 1
            await asyncio.sleep(1)


if __name__ == '__main__':
    import asyncio

    asyncio.run(send_message_to_bot('6760644170', 'hello'))
