#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: task.py
@time: 2025/3/28 17:15
"""
from celery import Celery
from commonts.settings import settings
from models.message import NewMessageModel
from loguru import logger
from celery_task.browser_manager.manager import BrowserManager
from config import get_config


browser_manager = BrowserManager(get_config())

# 配置 Celery
celery_app = Celery(
    'tasks',
    broker=settings.celery_broker,
    backend=settings.celery_backend,
    result_expires=3600
)


# 创建异步任务
@celery_app.task
def send_msg(new_msg: dict):
    new_msg = NewMessageModel(**new_msg)
    config = get_config()
    message = config.get('message')
    browser_manager.detail_msg(new_msg.phone_number, message)
    logger.info(f'send message {new_msg.phone_number},{message}')
    return 'OK'
