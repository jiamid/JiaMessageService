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
from models.message import MessageModel, MessagePageModel, SendMessageModel, FullMessageModel
from db.curd import DbService
from tg_bot.bot import send_message_to_bot
from fastapi.responses import StreamingResponse
import csv
import io
import asyncio

router = APIRouter()


class SendResponse(BaseResponseModel):
    data: str


@router.post('/send_msg', response_model=SendResponse)
async def send_msg(new_msg: SendMessageModel, background_tasks: BackgroundTasks):
    db = DbService()
    db.create_message(SendMessageModel(**new_msg.model_dump()))
    background_tasks.add_task(send_message_to_bot, chat_id=new_msg.chat_id, text=f'收到咨询:{new_msg.phone_number}',
                              parse_mode=None)
    return SendResponse(data=new_msg.session_id)


class PageResponse(BaseResponseModel):
    data: MessagePageModel


@router.get('/get_msg_page', response_model=PageResponse)
async def get_msg_page(chat_id: str, page: int = 0, size: int = 10, status: int = 0):
    if size > 100:
        raise ValueError('MaxSize:100')
    db = DbService()
    data = db.get_message_page(chat_id, page, size, status)
    return PageResponse(data=data)


class UpdateMessage(BaseModel):
    session_id: str
    status: int


@router.post('/update_msg_status', response_model=BaseResponseModel)
async def update_msg_status(update_msg: UpdateMessage):
    db = DbService()
    db.update_message_status(update_msg.session_id, update_msg.status)
    return BaseResponseModel()


class PendingMessageResponse(BaseResponseModel):
    data: FullMessageModel | None


@router.get('/get_pending_message', response_model=PendingMessageResponse)
async def get_pending_message(chat_id: str):
    db = DbService()
    one = db.get_one_pending_message(chat_id)
    return PendingMessageResponse(data=one)


@router.get('/export_csv/{chat_id}/{year}_{month}_{day}.csv')
async def get_csv_by_date(chat_id: str, year: int, month: int, day: int):
    db = DbService()
    data = db.get_message_data_by_date(chat_id, year, month, day)
    # Generate CSV stream
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=["session_id", "phone_number", "create_at"])
    writer.writeheader()
    writer.writerows(data)
    # Prepare filename (fixed the variable name from 'data' to 'day')
    filename = f"{chat_id}_{year}_{month}_{day}.csv"
    # Stream response
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",  # Changed from octet-stream to text/csv
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )
