# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 16:04
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : task_setting.py
# @Software: PyCharm
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.storage_manager import local_storage
from commonts.scheduler_manager import scheduler_manager
from commonts.settings import settings

logger.info('init join and exit')
@telegram_router.message(Command("join"))
async def join_team(message: Message) -> None:
    args = message.text.split()[1:]
    if not args:
        await message.answer("Pls With Password")
        return
    pwd = args[0]
    if pwd != settings.password:
        logger.info(f'{message.chat.id} join fail pwd error')
        await message.answer("Fail to join")
    else:
        local_storage.add_to_key('chat_ids', message.chat.id)
        logger.info(f'{message.chat.id} join success')
        await message.answer("Success to join")


@telegram_router.message(Command("exit"))
async def exit_item(message: Message) -> None:
    local_storage.del_from_key('chat_ids', message.chat.id)
    logger.info(f'{message.chat.id} exit success')
    await message.answer("Success to exit")
    chat_ids = local_storage.get_value('chat_ids', [])
    if not chat_ids:
        remove_status = scheduler_manager.remove_task('timer_scan')
        if remove_status:
            await message.answer("Remove timer_scan success")
            logger.info(f'timer_scan remove success')
        else:
            await message.answer("Remove timer_scan fail")
            logger.info(f'timer_scan remove fail')
