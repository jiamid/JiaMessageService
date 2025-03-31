#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: worker.py
@time: 2025/3/28 18:25
"""
from celery_task.task import celery_app
from commonts.logger import init_logging
from celery_task.browser_manager.manager import browser_manager

if __name__ == '__main__':
    init_logging('worker')
    browser_manager.init_browsers()
    celery_app.worker_main(['worker', '--loglevel=info'])
