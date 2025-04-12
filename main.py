# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 17:24
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : main.py
# @Software: PyCharm
from fastapi import FastAPI
from loguru import logger
from commonts.logger import init_logging
from commonts.settings import settings
from contextlib import asynccontextmanager
from api import router
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware


async def init_scheduler():
    from commonts.scheduler_manager import scheduler_manager
    logger.info("🚀 Starting scheduler")
    scheduler_manager.run()


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting Application")
    if settings.debug:
        logger.info(f"Docs http://127.0.0.1:{settings.port}/docs")
    yield
    logger.info("⛔ Stopping Application")


app = FastAPI(lifespan=lifespan,
              title='JiaMessageService',
              docs_url='/docs' if settings.debug else None,
              redoc_url='/redoc' if settings.debug else None,
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # 添加以下配置防止头部冲突
    expose_headers=["Content-Disposition"]
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    from uvicorn import run

    init_logging('service')
    run(app, host='0.0.0.0', port=settings.port)
