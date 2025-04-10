#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: message.py
@time: 2025/3/28 17:23
"""
from fastapi import APIRouter, BackgroundTasks
from loguru import logger
from commonts.settings import settings
from pydantic import BaseModel
from models.base_model import BaseResponseModel
from models.message import MessageModel, MessagePageModel, SendMessageModel
from db.curd import DbService
from tg_bot.bot import send_message_to_bot

router = APIRouter()


class SendResponse(BaseResponseModel):
    data: str


@router.post('/send_msg', response_model=SendResponse)
async def send_msg(new_msg: SendMessageModel, background_tasks: BackgroundTasks):
    db = DbService()
    db.create_message(MessageModel(**new_msg.model_dump()))
    background_tasks.add_task(send_message_to_bot, chat_id=new_msg.chat_id, text=f'收到咨询:{new_msg.phone_number}',
                              parse_mode=None)
    return SendResponse(data=new_msg.session_id)


class PageResponse(BaseResponseModel):
    data: MessagePageModel


@router.get('/get_msg_page', response_model=PageResponse)
async def get_msg_page(page: int = 0, size: int = 10, status: int = 0):
    if size > 100:
        raise ValueError('MaxSize:100')
    db = DbService()
    data = db.get_message_page(page, size, status)
    return PageResponse(data=data)


class UpdateMessage(BaseModel):
    session_id: str
    status: int


@router.post('/update_msg_status', response_model=BaseResponseModel)
async def update_msg_status(update_msg: UpdateMessage):
    db = DbService()
    db.update_message_status(update_msg.session_id, update_msg.status)
    return BaseResponseModel()
