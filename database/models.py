from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, unique=True)
    ban = Column(Integer, default=0)
    join_link = Column(DateTime)
    join_date = Column(DateTime)
    city = Column(String)
    platform = Column(String)
    subscription = Column(Integer, default=0)


class Link(Base):
    __tablename__: str = 'links'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    city = Column(String)
    platform = Column(String)
    link = Column(String, unique=True)
    users = Column(Text)
    date = Column(String)


class Channel(Base):
    __tablename__ = 'channels'
    chat_id = Column(BigInteger, primary_key=True, unique=True)
    city = Column(String)  # city name
    invite_link = Column(String)
    manager = Column(String)


class Platform(Base):
    __tablename__ = 'platforms'
    platform_name = Column(String, primary_key=True, unique=True)
