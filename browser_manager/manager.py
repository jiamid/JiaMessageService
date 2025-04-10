#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: manager.py
@time: 2025/3/29 08:19
"""

import time
import random
import traceback
import urllib3
import requests
from loguru import logger
from browser_manager.api import AdsApi
from DrissionPage import ChromiumOptions, Chromium

urllib3.disable_warnings()


class BrowserManager:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            print("初始化BrowserManager")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_pre, max_browser_num: int = 1):
        self.api_pre = api_pre
        self.ads_api = AdsApi()

        self.max_browser_num = max_browser_num
        self.one_browser_max_task = 4
        self.browser_gen = self.gen_new_browser()

        self.task_index = 0
        self.running_browsers = {}
        self.running_browsers_times = {}

    def init_browsers(self):
        self.running_browsers_times = {}
        for i in range(self.max_browser_num):
            self.running_browsers[i] = self.browser_gen.__next__()

    def update_message_status(self, session_id: str, status: int):
        api = f'{self.api_pre}/update_browser_status'
        body = {
            'session_id': session_id,
            'status': status
        }
        resp = requests.post(api, json=body)
        logger.info(resp)

    def get_pending_message(self):
        api = f'{self.api_pre}/get_pending_message'
        resp = requests.get(api)
        data = resp.json()
        message_info = data.get('data', None)
        return message_info

    def update_browser_status(self, browser_id: str, status: int, detail: str = ''):
        api = f'{self.api_pre}/update_browser_status'
        body = {
            'browser_id': browser_id,
            'status': status
        }
        resp = requests.post(api, json=body)
        logger.info(resp)

    def get_pending_browser(self):
        api = f'{self.api_pre}/get_pending_browser'
        resp = requests.get(api)
        data = resp.json()
        browser_info = data.get('data', None)
        if browser_info:
            browser_id = browser_info.get('browser_id')
            last_used_at = browser_info.get('last_used_at')
            now = time.time()
            if last_used_at + (3600 * 8) < now:
                self.update_browser_status(browser_id, 2)
                return browser_id
        logger.warning(f'空闲浏览器不足')
        return None

    def gen_new_browser(self):
        while True:
            browser_id = self.get_pending_browser()
            try:
                if browser_id:
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
                else:
                    logger.info(f'无空闲浏览器睡眠10s')
                    time.sleep(10)
            except Exception as e:
                self.update_browser_status(browser_id, 3, str(e))
                logger.error(f'GenBrowseFail:ID_{browser_id},Error:{traceback.format_exc()}')

    def close_browser(self, index, status=1, detail=''):
        browser_info = self.running_browsers.get(index)
        if browser_info:
            browser_id = browser_info.get('id')
            self.update_browser_status(browser_id, status, detail)
            self.ads_api.stop_browser(browser_info.get('id'))
            logger.info(f'关闭浏览器ID{browser_info.get('id')}')

    def get_browser(self):
        self.task_index = self.task_index % self.max_browser_num
        browser = self.running_browsers.get(self.task_index, None)
        if browser is None:
            browser = self.browser_gen.__next__()
            self.running_browsers[self.task_index] = browser
        return browser

    def commit(self, status=1, detail=''):
        now_times = self.running_browsers_times.get(self.task_index, 0) + 1
        self.running_browsers_times[self.task_index] = now_times
        if now_times == self.one_browser_max_task:
            # browser.close()
            logger.info(f'关闭浏览器{self.task_index}')
            self.close_browser(self.task_index, status, detail)
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

    def detail_msg(self, phone_number: str, msg):
        if phone_number.startswith('00'):
            phone_number = phone_number[2:]
        browser_info = self.get_browser()
        status = 1
        detail = ''
        try:
            self.send_msg(browser_info, phone_number, msg)
        except Exception as e:
            status = 3
            detail = f'{e.__str__()}'
        self.commit(status, detail)
        return True if status == 1 else False

    def run(self):
        while True:
            message_info = self.get_pending_message()
            if message_info:
                session_id = message_info.get('session_id')
                msg = message_info.get('msg')
                phone_number = message_info.get('phone_number')
                try:
                    self.update_message_status(session_id,2)
                    do_status =self.detail_msg(phone_number, msg)
                    if do_status:
                        self.update_message_status(session_id,4)
                    else:
                        self.update_message_status(session_id, 3)
                except Exception as e:
                    logger.error(f'SendMsgError:{e}')
                    self.update_message_status(session_id, 3)
            else:
                logger.info(f'暂无消息，睡眠10s')
                time.sleep(10)


