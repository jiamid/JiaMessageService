#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: browser.py
@time: 2025/3/28 19:02
"""
from enum import IntEnum
from pydantic import BaseModel, Field
from datetime import datetime


class BrowserStatusType(IntEnum):
    Pending = 1
    Running = 2
    Error = 3


class BrowserModel(BaseModel):
    browser_id: str = Field()


class FullBrowserModel(BrowserModel):
    status: int = Field()
    detail: str = Field()
    created_at: datetime = Field()
    last_used_at: int = Field()

    class Config:
        from_attributes = True


class BrowserPageModel(BaseModel):
    browsers: list[FullBrowserModel] = Field()
    count: int = Field()
    page: int = Field()
    size: int = Field()
