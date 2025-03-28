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

# 配置 Celery
celery_app = Celery(
    'tasks',
    broker=settings.celery_broker,
    backend=settings.celery_backend,
    result_expires=3600
)


# 创建异步任务
@celery_app.task
def send_msg(new_msg: NewMessageModel | dict):
    new_msg = NewMessageModel(**new_msg)
    logger.info(f'SendMsgTo:{new_msg.phone_number},Msg:{new_msg.msg}')
