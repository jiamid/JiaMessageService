#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: html.py
@time: 2025/4/7 16:38
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=RedirectResponse)
async def index(request: Request):
    context = {
        "request": request,  # 必须包含request
    }
    return templates.TemplateResponse("index.html", context)


@router.get("/message/{chat_id}", response_class=HTMLResponse)
async def go_message(chat_id: str, request: Request):
    context = {
        "request": request,  # 必须包含request
        "chat_id": chat_id,  # 路径参数
    }
    return templates.TemplateResponse("message.html", context)


@router.get("/browser/{chat_id}", response_class=HTMLResponse)
async def go_browser(chat_id: str, request: Request):
    context = {
        "request": request,  # 必须包含request
        "chat_id": chat_id,  # 路径参数
    }
    return templates.TemplateResponse("browser.html", context)
