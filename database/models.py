from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):

    """
    База для Алхимии, от нее будет наследоваться все остальное
    """

    pass


class User(Base):

    """
    Все данные для пользователя

    :param user_id: его id (тип `BigInteger`)
    :param ban: заблокировал ли бота (по умолчанию 0 — не заблокирован)
    :param join_link: пригласительная ссылка, по которой попал в бота (тип `String`)
    :param join_date: дата, когда пользователь присоединился (тип `DateTime`)
    :param city: название города, откуда юзер (тип `String`)
    :param platform: платформа, с которой пришел пользователь по ссылке (тип `String`)
    :param subscription: подписан ли на канал (1 — активен, 0 — не активен, по умолчанию 0)

    """

    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True)
    ban = Column(Integer, default=0)
    join_link = Column(String)
    join_date = Column(DateTime)
    city = Column(String)
    platform = Column(String)
    subscription = Column(Integer, default=0)


class Link(Base):

    """
    Пригласительные ссылки

    :param id: id ссылки, auto increase в базе (тип `BigInteger`, автогенерация)
    :param name: название ссылки, уникальное, любое для работы (тип `String`, уникальное)
    :param city: город ссылки (тип `String`)
    :param platform: платформа ссылки (тип `String`)
    :param link: сама ссылка (тип `String`, уникальное)
    :param users: список пользователей, которые пришли по ссылке (тип `Text`)
    :param date: дата создания ссылки (тип `String`)

    """

    __tablename__: str = 'links'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    city = Column(String)
    platform = Column(String)
    link = Column(String, unique=True)
    users = Column(Text)
    date = Column(String)


class Channel(Base):

    """
    Наши каналы или города

    :param chat_id: id канала (тип `BigInteger`, уникальное)
    :param city: город канала (тип `String`)
    :param invite_link: пригласительная ссылка канала (тип `String`)
    :param manager: менеджер этого канала (тип `String`)
    """

    __tablename__ = 'channels'

    chat_id = Column(BigInteger, primary_key=True, unique=True)
    city = Column(String)  # city name
    invite_link = Column(String)
    manager = Column(String)


class Platform(Base):

    """
    Платформы, откуда люди будут приходить
    Старое решение, на скорую руку

    :param platform_name: название платформы (тип `String`, уникальное)
    """
    __tablename__ = 'platforms'

    platform_name = Column(String, primary_key=True, unique=True)
