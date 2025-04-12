#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Jiamid
@Contact: JiamidTan@poweronlabs.ai
@file: client.py
@time: 2025/4/7 11:39
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, BigInteger, JSON, UniqueConstraint, TIMESTAMP
from commonts.settings import settings

# SQLAlchemy配置
DATABASE_URL = f"sqlite:///./{settings.db_name}.db"  # 使用SQLite数据库

# 创建SQLAlchemy引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


# 数据模型
class MessageTable(Base):
    __tablename__ = 'message'

    session_id = Column(String, primary_key=True, index=True)
    phone_number = Column(String)
    chat_id = Column(String)
    msg = Column(String)
    status = Column(Integer, default=1)# Pending = 1 Running = 2 Error = 3 Success = 4
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


class BrowserTable(Base):
    __tablename__ = 'browser'

    id = Column(Integer, primary_key=True, autoincrement=True)
    browser_id = Column(String)
    chat_id = Column(String)
    detail = Column(String, default='')
    status = Column(Integer, default=1)  # 1正常 2使用中 3异常
    last_used_at = Column(BigInteger, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


# 创建数据库表
Base.metadata.create_all(bind=engine)
