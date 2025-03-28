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

async def init_scheduler():
    from commonts.scheduler_manager import scheduler_manager
    logger.info("🚀 Starting scheduler")
    scheduler_manager.run()

async def init_tg_webhook():
    from tg_bot.bot import bot
    from tg_bot import handlers
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != f'{settings.base_webhook_url}{settings.webhook_path}':
        logger.info(f'set webhook {settings.webhook_path}')
        await bot.set_webhook(
            url=f'{settings.base_webhook_url}{settings.webhook_path}',
            secret_token=settings.secret_token,
            drop_pending_updates=True,
            max_connections=100,
        )

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting Application")
    if settings.debug:
        logger.info(f"Docs http://127.0.0.1:{settings.port}/docs")
    # await init_tg_webhook()
    # await init_scheduler()
    yield
    logger.info("⛔ Stopping Application")


app = FastAPI(lifespan=lifespan,
              title='JiaMessageService',
              docs_url='/docs' if settings.debug else None,
              redoc_url='/redoc' if settings.debug else None,
              )
app.include_router(router)

if __name__ == '__main__':
    from uvicorn import run
    init_logging()
    run(app, host='0.0.0.0', port=settings.port)
