# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 15:22
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : local_main.py
# @Software: PyCharm
from tg_bot.bot import bot, dp
from tg_bot import handlers


async def start_test():
    await bot.delete_webhook(drop_pending_updates=True)
    print('webhook is del')
    print('Bot Start')
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(start_test())
