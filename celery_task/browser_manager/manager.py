#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: manager.py
@time: 2025/3/29 08:19
"""
import asyncio
import json
import multiprocessing
import os
import platform
import sys
import time
import random
import urllib3
from functools import wraps
from loguru import logger
import requests
from celery_task.browser_manager.api import AdsApi
from DrissionPage import ChromiumPage, ChromiumOptions, Chromium
from DrissionPage.common import Keys
from DrissionPage.common import Actions

urllib3.disable_warnings()


class BrowserManager:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            print("初始化BrowserManager")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.ads_api = AdsApi()
        self.browser_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.running_browsers = {}
        self.running_browsers_times = []
        self.task_index = 0
        self.max_browser_num = 2
        self.one_browser_max_task = 4
        if self.max_browser_num > len(self.browser_list):
            raise ValueError('允许运行浏览器数量大于实际浏览器数量!')
        self.browser_gen = self.gen_new_browser()
        self.init_browsers()

    def init_browsers(self):
        self.running_browsers_times = [0 for i in range(self.max_browser_num)]
        for i in range(self.max_browser_num):
            self.running_browsers[i] = self.browser_gen.__next__()

    def gen_new_browser(self):
        while True:
            for browser_id in self.browser_list:
                # cdp_url = self.ads_api.start_browser(browser_id)
                # port = cdp_url.split(':')[-1]
                # browser = Chromium(int(port))
                browser = browser_id
                yield browser

    def get_browser(self):
        self.task_index = self.task_index % self.max_browser_num
        browser = self.running_browsers.get(self.task_index)
        return browser

    def commit(self,browser):
        now_times = self.running_browsers_times[self.task_index] + 1
        self.running_browsers_times[self.task_index] = now_times
        if now_times == self.one_browser_max_task:
            # browser.close()
            logger.info(f'关闭浏览器{self.task_index},ID:{browser}')
            self.running_browsers[self.task_index] = self.browser_gen.__next__()
            self.running_browsers_times[self.task_index] = 0
            logger.info(f'更新第{self.task_index}浏览器')
        self.task_index += 1

    def detail_msg(self, phone_number, msg):
        browser = self.get_browser()
        logger.info(f'Use {browser} SendMsg:{msg},To:{phone_number}')
        self.commit(browser)

browser_manager = BrowserManager()

if __name__ == '__main__':
    for x in range(1000):
        logger.info(f'Send Msg{x}')
        browser_manager.detail_msg('123','hello')