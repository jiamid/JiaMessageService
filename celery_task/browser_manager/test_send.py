#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: test_send.py
@time: 2025/3/30 21:23
"""
from DrissionPage import ChromiumOptions, Chromium
from DrissionPage.common import Keys


def send_msg(browser, phone_no, msg):
    tab = browser.latest_tab()
    tab.get(f"https://web.whatsapp.com/send?phone={phone_no}")
    tab.actions.click('#kw').input('DrissionPage')
    tab.actions.key_up('ENTER')  # 输入按键名称
    tab.actions.key_up(Keys.ENTER)


if __name__ == '__main__':
    new_browser = Chromium()
    send_msg(new_browser, '16195360670', 'helloworld')
