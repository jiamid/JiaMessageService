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
from celery_task.task import add

router = APIRouter()


class TaskResponse(BaseResponseModel):
    data: str = ''


@router.post('/add_task', response_model=TaskResponse)
async def add_task(a: int, b: int):
    task_id = add.deta()
    return TaskResponse(data=task_id)
