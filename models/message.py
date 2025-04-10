#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: message.py
@time: 2025/3/28 19:02
"""
from enum import IntEnum
from pydantic import BaseModel, Field
from datetime import datetime


class MessageStatusType(IntEnum):
    Pending = 1
    Running = 2
    Error = 3
    Success = 4


class MessageModel(BaseModel):
    session_id: str = Field()
    phone_number: str = Field()
    msg: str = Field()


class SendMessageModel(MessageModel):
    chat_id: str = Field()


class FullMessageModel(MessageModel):
    status: int = Field()
    created_at: datetime = Field()

    class Config:
        use_enum_values = True
        from_attributes = True


class MessagePageModel(BaseModel):
    messages: list[FullMessageModel] = Field()
    count: int = Field()
    page: int = Field()
    size: int = Field()
