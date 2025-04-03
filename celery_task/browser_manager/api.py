#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: api.py
@time: 2025/3/29 11:48
"""
import asyncio
import time
import random
import functools
import traceback
import requests

from loguru import logger


class JiaDecorator:
    """
    修饰器，用于控制同一请求速度，避免并发请求
    @TaskTimeDecorator.async_timing_decorator
    """
    task_last_time = {}

    @staticmethod
    def async_timing_decorator(func):
        async def wrapper(*args, **kwargs):
            this_name = func.__name__
            now = time.time()
            last = JiaDecorator.task_last_time.get(this_name, 0)
            if last > now - 1:
                await asyncio.sleep(1)
                return await wrapper(*args, **kwargs)
            JiaDecorator.task_last_time[this_name] = now
            result = await func(*args, **kwargs)
            return result

        return wrapper

    @staticmethod
    def sync_timing_decorator(func):
        def wrapper(*args, **kwargs):
            this_name = func.__name__
            now = time.time()
            last = JiaDecorator.task_last_time.get(this_name, 0)
            if last > now - 1:
                time.sleep(1)
                return wrapper(*args, **kwargs)
            JiaDecorator.task_last_time[this_name] = now
            result = func(*args, **kwargs)
            return result

        return wrapper

    @staticmethod
    def repeat_times(times=3):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for now_times in range(1, times + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        sleep_time = round(random.uniform(2, 5), 1)
                        if now_times == times:  # 如果是最后一次失败，直接抛出异常
                            raise ValueError(f"重试超过 {times} 次，最终失败") from e
                        logger.warning(f"第 {now_times} 次执行失败,睡眠:{sleep_time},Error:\n{traceback.format_exc()}")
                        time.sleep(sleep_time)

            return wrapper

        return decorator


class AdsApi:
    def __init__(self):
        self.headers = {
            'user-agent': 'Jiamid/SubTaskClient 1.0'
        }
        self.api_base = 'http://local.adspower.net:50325'

    @JiaDecorator.repeat_times(3)
    def _request(self, method, api, payload=None, data=None, params=None, times=3):
        try:
            response = requests.request(
                method=method,
                url=api,
                json=payload,
                data=data,
                params=params,
                verify=False,
                headers=self.headers
            )
            return response.json()
        except Exception as e:
            logger.error(f'Network Exception: {e}')
            times -= 1
            if times < 0:
                logger.error(f'{method}网络异常: {api}, {e}')
                return {}
            time.sleep(1)
            logger.info(f'重发: {api}')
            res_data = self._request(method, api, payload, data, params, times)
            return res_data

    def request_post(self, api, payload=None, data=None, times=3):
        return self._request('POST', api, payload=payload, data=data, times=times)

    def request_get(self, api, params=None, times=3):
        return self._request('GET', api, params=params, times=times)

    @JiaDecorator.sync_timing_decorator
    def start_browser(self, b_id):
        api = f'{self.api_base}/api/v1/browser/start'
        payload = {
            "user_id": b_id,
            "cdp_mask": 1
        }
        res_data = self.request_get(api, payload)
        if res_data:
            logger.info(f'start_browser {res_data}')
            data = res_data.get('data', {})
            if data:
                cdp_url = data.get('ws', {}).get('selenium', None)
                port = data.get('debug_port', None)
                webdriver = data.get('webdriver', None)
                return {'port': port, 'webdriver': webdriver}
        return None

    @JiaDecorator.sync_timing_decorator
    def stop_browser(self, b_id):
        api = f'{self.api_base}/api/v1/browser/stop'
        payload = {
            "user_id": b_id,
        }
        times = 3
        while times > 0:
            res_data = self.request_get(api, payload)
            logger.info(f'stop_browser_resp {b_id}: {res_data}')
            if res_data.get('code', -1) == 0:
                logger.info(f'stop_browser {b_id} success')
                break
            time.sleep(1)
            times -= 1
            logger.info(f'stop_browser {b_id} fail, try again')
