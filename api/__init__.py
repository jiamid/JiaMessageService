# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:19
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from fastapi import APIRouter
from api.message import router as msg_router
from api.browser import router as browser_router
from api.html import router as index_router

router = APIRouter()
router.include_router(index_router)
router.include_router(msg_router)
router.include_router(browser_router)
