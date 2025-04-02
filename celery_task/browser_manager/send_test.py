#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: send_test.py
@time: 2025/3/30 21:23
"""
import time

from DrissionPage import ChromiumOptions, Chromium
from DrissionPage.common import Keys
from celery_task.browser_manager.api import AdsApi


# cdp_url = self.ads_api.start_browser(browser_id)
                # port = cdp_url.split(':')[-1]
                # browser = Chromium(int(port))

def start_browser(b_id):
    ads_api = AdsApi()
    cdp_url = ads_api.start_browser(b_id)
    return cdp_url

def send_msg(browser, phone_no, msg):
    tab = browser.latest_tab
    tab.get(f"https://web.whatsapp.com/send?phone={phone_no}")
    time.sleep(2)
    ele_input = 'xpath://div[@id="main"]//div[@role="textbox"]'
    e = tab.ele(ele_input,timeout=15)
    e.input(f'{msg}\n')
    print('ok')


if __name__ == '__main__':
    #cdp = start_browser('jhnmm4m')
    #port = cdp.split(':')[-1]
    #print(cdp)
    port = 54247
    c_path = 'C:\\Users\\Administrator\\AppData\\Roaming\\adspower_global\\cwd_global\\chrome_124\\chromedriver.exe'
    opts = ChromiumOptions()
    opts.set_browser_path(c_path)
    opts.set_paths(local_port=54247)
    new_browser = Chromium(opts)
    a = '12897437693'
    b = ''
    send_msg(new_browser, '12897437693', 'yes i do')
