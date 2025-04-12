#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: message.py
@time: 2025/3/28 19:02
"""
from enum import IntEnum
from pydantic import BaseModel, Field,model_validator
from datetime import datetime
from zoneinfo import ZoneInfo


class MessageStatusType(IntEnum):
    Pending = 1
    Running = 2
    Error = 3
    Success = 4


class MessageModel(BaseModel):
    session_id: str = Field()
    phone_number: str = Field()
    chat_id: str = Field(min_length=3)
    msg: str = Field(default='')


class SendMessageModel(MessageModel):
    pass


class FullMessageModel(MessageModel):
    status: int = Field()
    created_at: datetime = Field()
    created_at_str:str = Field(default='')

    @model_validator(mode='after')
    def set_created_at_str(self) -> 'FullMessageModel':
        """自动生成 UTC+8 时区的时间字符串"""
        # 确保有时区信息（假设无时区的是UTC）
        if self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=ZoneInfo('UTC'))

        # 转换为 UTC+8（如北京时间）
        beijing_time = self.created_at.astimezone(ZoneInfo('Asia/Shanghai'))
        self.created_at_str = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

        return self


    class Config:
        use_enum_values = True
        from_attributes = True


class MessagePageModel(BaseModel):
    messages: list[FullMessageModel] = Field()
    count: int = Field()
    page: int = Field()
    size: int = Field()
