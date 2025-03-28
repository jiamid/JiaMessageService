# -*- coding: utf-8 -*-
# @Time    : 2024/7/26 17:18
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : messages.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from loguru import logger
from aiogram import types
from aiogram import F
import re
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from commonts.util import to_escape_string
from tg_bot.bot import telegram_router

logger.info('init message')


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id},Chat ID: {message.chat.id}")


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'*Hello {to_escape_string(message.from_user.first_name)}*', parse_mode='MarkdownV2')


@telegram_router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(f'*Hello {to_escape_string(message.from_user.first_name)}*\n'
                         f'\n\n', parse_mode='MarkdownV2')
