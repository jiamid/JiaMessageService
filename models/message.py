#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: message.py
@time: 2025/3/28 19:02
"""
from pydantic import BaseModel,Field

class NewMessageModel(BaseModel):
    phone_number:str
    msg:str