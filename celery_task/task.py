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

# 配置 Celery
celery_app = Celery(
    'tasks',
    broker=settings.redis_broker,
    backend=settings.redis_backend
)


# 创建异步任务
@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def multiply(x, y):
    return x * y
