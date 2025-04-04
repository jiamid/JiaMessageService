#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: task.py
@time: 2025/3/28 17:23
"""
from fastapi import APIRouter
from loguru import logger
from commonts.settings import settings
from commonts.base_model import BaseResponseModel
from celery_task.task import send_msg
from models.message import NewMessageModel

router = APIRouter()


class TaskResponse(BaseResponseModel):
    data: str = ''


@router.post('/add_task', response_model=TaskResponse)
async def add_task(new_msg:NewMessageModel):
    logger.info(f'shoudao:{new_msg}')
    task_id = send_msg.apply_async(kwargs={'new_msg':new_msg.model_dump()})
    task_id = str(task_id)
    return TaskResponse(data=task_id)
