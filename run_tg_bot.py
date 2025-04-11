#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: run_tg_bot.py
@time: 2025/4/11 21:51
"""
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 15:22
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : local_main.py
# @Software: PyCharm
from tg_bot.bot import bot, dp


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot Start')
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(start_bot())
