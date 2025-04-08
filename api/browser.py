#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: browser.py
@time: 2025/3/28 17:23
"""
from fastapi import APIRouter
from loguru import logger
from commonts.settings import settings
from pydantic import BaseModel
from models.base_model import BaseResponseModel
from models.browser import BrowserPageModel, BrowserModel
from db.curd import DbService

router = APIRouter()




@router.post('/add_browser', response_model=BaseResponseModel)
async def add_browser(new: BrowserModel):
    db = DbService()
    status = db.create_browser(new)
    msg = f'创建成功:{new.browser_id}'
    if not status:
        msg = f'{new.browser_id}已存在'
    return BaseResponseModel(msg=msg)


class PageResponse(BaseResponseModel):
    data: MessagePageModel


@router.get('/get_msg_page', response_model=PageResponse)
async def get_msg_page(page: int = 0, size: int = 10, status: int = 0):
    db = DbService()
    data = db.get_message_page(page, size, status)
    return PageResponse(data=data)


class UpdateMessage(BaseModel):
    session_id: str
    status: int


@router.post('/update_msg_page', response_model=BaseResponseModel)
async def update_msg_page(update_msg: UpdateMessage):
    db = DbService()
    db.update_message_status(update_msg.session_id, update_msg.status)
    return BaseResponseModel()
