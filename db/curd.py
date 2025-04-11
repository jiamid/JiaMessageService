#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: curd.py
@time: 2025/3/4 12:13
"""
import time
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from loguru import logger
from db.client import SessionLocal
from contextlib import contextmanager
from db.client import MessageTable, BrowserTable

from models.message import MessageModel, FullMessageModel, MessagePageModel,SendMessageModel
from models.browser import BrowserModel, FullBrowserModel, BrowserPageModel


class DbService:
    def __init__(self):
        self.session_local = SessionLocal

    @contextmanager
    def get_session(self):
        session = self.session_local()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_message(self, new: SendMessageModel):
        with self.get_session() as session:
            data = new.model_dump()
            old = session.query(MessageTable).filter(MessageTable.session_id == new.session_id).first()
            if old:
                logger.info(f'Message:{new.session_id}已存在')
                return
            session.add(MessageTable(**data))

    def create_browser(self, new: BrowserModel):
        with self.get_session() as session:
            data = new.model_dump()
            old = session.query(BrowserTable).filter(BrowserTable.browser_id == new.browser_id).first()
            if old:
                logger.info(f'Browser:{new.browser_id}已存在')
                return False
            session.add(BrowserTable(**data))
        return True

    def get_message_page(self, page: int = 0, size: int = 10, status: int = 0):
        with self.get_session() as session:
            query = session.query(MessageTable)
            if status > 0:
                query = query.filter(MessageTable.status == status)
            message_objs = query.order_by(MessageTable.created_at.desc()).offset(page * size).limit(size).all()
            count = query.count()
            messages = [FullMessageModel.model_validate(obj) for obj in message_objs] if message_objs else []
            data = MessagePageModel(
                messages=messages,
                count=count,
                page=page,
                size=size
            )
            return data

    def get_browser_page(self, page: int = 0, size: int = 10, status: int = 0):
        with self.get_session() as session:
            query = session.query(BrowserTable)
            if status > 0:
                query = query.filter(BrowserTable.status == status)
            browser_objs = query.order_by(BrowserTable.created_at.desc()).offset(page * size).limit(size).all()
            count = query.count()
            browsers = [FullBrowserModel.model_validate(obj) for obj in browser_objs] if browser_objs else []
            data = BrowserPageModel(
                browsers=browsers,
                count=count,
                page=page,
                size=size
            )
            return data

    def update_message_status(self, session_id: str, status: int):
        with self.get_session() as session:
            session.query(MessageTable).filter(
                MessageTable.session_id == session_id
            ).update({
                MessageTable.status: status
            })

    def update_browser_status(self, browser_id: str, status: int, detail: str):
        if status == 5:
            status = 1
            last_used_at = 0
        else:
            last_used_at = int(time.time())
        with self.get_session() as session:
            session.query(BrowserTable).filter(
                BrowserTable.browser_id == browser_id
            ).update({
                BrowserTable.status: status,
                BrowserTable.last_used_at: last_used_at,
                BrowserTable.detail: detail
            })

    def delete_message_by_id(self, session_id: int):
        with self.get_session() as session:
            session.query(MessageTable).filter(
                MessageTable.session_id == session_id
            ).delete()

    def delete_browser_by_id(self, browser_id: int):
        with self.get_session() as session:
            session.query(BrowserTable).filter(
                BrowserTable.browser_id == browser_id
            ).delete()

    def get_one_pending_message(self):
        with self.get_session() as session:
            pending_one = session.query(MessageTable).filter(
                MessageTable.status == 1
            ).order_by(MessageTable.created_at.asc()).first()
            if pending_one:
                new_one = FullMessageModel.model_validate(pending_one)
                return new_one
        return None

    def get_one_pending_browser(self):
        with self.get_session() as session:
            pending_one = session.query(BrowserTable).filter(
                BrowserTable.status == 1
            ).order_by(BrowserTable.last_used_at.asc()).first()
            if pending_one:
                new_one = FullBrowserModel.model_validate(pending_one)
                return new_one
        return None
