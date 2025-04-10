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
from models.browser import BrowserPageModel, BrowserModel, FullBrowserModel
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
    data: BrowserPageModel


@router.get('/get_browser_page', response_model=PageResponse)
async def get_browser_page(page: int = 0, size: int = 10, status: int = 0):
    db = DbService()
    data = db.get_browser_page(page, size, status)
    return PageResponse(data=data)


class UpdateBrowser(BaseModel):
    browser_id: str
    status: int
    detail: str = ''


@router.post('/update_browser_status', response_model=BaseResponseModel)
async def update_browser_status(update_data: UpdateBrowser):
    db = DbService()
    db.update_browser_status(update_data.browser_id, update_data.status, update_data.detail)
    return BaseResponseModel()


class PendingBrowserResponse(BaseResponseModel):
    data: FullBrowserModel | None


@router.get('/get_pending_browser', response_model=PendingBrowserResponse)
async def get_pending_browser():
    db = DbService()
    one = db.get_one_pending_browser()
    return PendingBrowserResponse(data=one)
