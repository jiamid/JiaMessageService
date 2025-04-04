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
import traceback
import urllib3
from loguru import logger
from celery_task.browser_manager.api import AdsApi
from DrissionPage import ChromiumOptions, Chromium

urllib3.disable_warnings()


class BrowserManager:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            print("初始化BrowserManager")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,config:dict):
        self.ads_api = AdsApi()
        self.browser_list = config.get('ads_ids')
        self.task_index = 0
        self.max_browser_num = 1
        self.one_browser_max_task = 4
        if self.max_browser_num > len(self.browser_list):
            raise ValueError('允许运行浏览器数量大于实际浏览器数量!')
        self.browser_gen = self.gen_new_browser()

        self.running_browsers = {}
        self.running_browsers_times = {}

    def init_browsers(self):
        self.running_browsers_times = {}
        for i in range(self.max_browser_num):
            self.running_browsers[i] = self.browser_gen.__next__()

    def gen_new_browser(self):
        while True:
            for browser_id in self.browser_list:
                try:
                    browser_data = self.ads_api.start_browser(browser_id)
                    if not browser_data:
                        continue
                    opts = ChromiumOptions()
                    opts.set_browser_path(browser_data.get('webdriver'))
                    opts.set_paths(local_port=int(browser_data.get('port')))
                    new_browser = Chromium(opts)
                    logger.info(f'GenBrowserId:{browser_id}')
                    yield {
                        'id': browser_id,
                        'browser': new_browser
                    }
                except Exception as e:
                    logger.error(f'GenBrowseFail:ID_{browser_id},Error:{traceback.format_exc()}')

    def close_browser(self, index):
        browser_info = self.running_browsers.get(index)
        if browser_info:
            self.ads_api.stop_browser(browser_info.get('id'))
            logger.info(f'关闭浏览器ID{browser_info.get('id')}')

    def get_browser(self):
        self.task_index = self.task_index % self.max_browser_num
        browser = self.running_browsers.get(self.task_index, None)
        if browser is None:
            browser = self.browser_gen.__next__()
            self.running_browsers[self.task_index] = browser
        return browser

    def commit(self):
        now_times = self.running_browsers_times.get(self.task_index, 0) + 1
        self.running_browsers_times[self.task_index] = now_times
        if now_times == self.one_browser_max_task:
            # browser.close()
            logger.info(f'关闭浏览器{self.task_index}')
            self.close_browser(self.task_index)
            self.running_browsers[self.task_index] = self.browser_gen.__next__()
            self.running_browsers_times[self.task_index] = 0
            logger.info(f'更新第{self.task_index}浏览器')
        self.task_index += 1

    def send_msg(self, browser_info, phone_number, msg):
        b_id = browser_info.get('id')
        browser = browser_info.get('browser')
        tab = browser.latest_tab
        tab.get(f"https://web.whatsapp.com/send?phone={phone_number}")
        time.sleep(3)
        ele_input = 'xpath://div[@id="main"]//div[@role="textbox"]'
        e = tab.ele(ele_input, timeout=25)
        e.input(f'{msg}\n')
        logger.info(f'Use {b_id} SendMsg:{msg},To:{phone_number}')

    def detail_msg(self, phone_number:str, msg):
        if phone_number.startswith('00'):
            phone_number = phone_number[2:]
        browser_info = self.get_browser()
        self.send_msg(browser_info, phone_number, msg)
        self.commit()



if __name__ == '__main__':
    from config import get_config
    browser_manager = BrowserManager(get_config())
    for x in range(1000):
        logger.info(f'Send Msg{x}')
        browser_manager.detail_msg('123', 'hello')
