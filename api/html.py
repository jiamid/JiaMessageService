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


@router.get("/message", response_class=HTMLResponse)
async def go_message(request: Request):
    return templates.TemplateResponse("message.html", {"request": request})

@router.get("/browser", response_class=HTMLResponse)
async def go_browser(request: Request):
    return templates.TemplateResponse("browser.html", {"request": request})