from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update, values
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Link, Channel, Platform


async def add_user(session: AsyncSession, user_id: int, join_link, city, platform):

    """

    :param session: бд сессия
    :param user_id: id юзера
    :param join_link: пригласительная ссылка
    :param city: город юзера
    :param platform: платформа, где была ссылка
    :return:
    """

    # создаем дата объект
    join_date = datetime.now()

    # заполняем данные для юзера
    new_user = User(user_id=user_id,
                    ban=0,
                    join_link=join_link,
                    join_date=join_date,
                    city=city,
                    platform=platform)

    # добавляем и пробуем закомитить
    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()


async def get_user(session: AsyncSession, user_id: int):
    """
    Получает пользователя по его ID из базы данных.

    :param session: бд сессия
    :param user_id: ID пользователя, которого нужно найти
    :return: Пользователь (User объект), если найден, иначе None
    """
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar()


async def db_create_link(session: AsyncSession, name: str, city: str, platform: str, link_prefix: str):
    """
    Создает новую ссылку и сохраняет её в базе данных, добавляя префикс к ссылке.

    :param session: бд сессия
    :param name: Имя ссылки
    :param city: Город ссылки
    :param platform: Платформа, где будет размещаться ссылка
    :param link_prefix: Это типа id уникальный, auto increase в бд
    :return: Ссылку, если была создана, или ошибку уникальности по имени, или None
    """

    # создаем дату с учетом мск времени (+3 часа)
    date = datetime.now(timezone(timedelta(hours=3))).isoformat()

    # заполняем данные ссылки
    new_link = Link(name=name, city=city, platform=platform, date=date)

    # добавляем в сессию и пробуем комит
    session.add(new_link)

    # создаем в бд, возвращаем id из auto increase и вставляем в ссылку
    try:
        await session.commit()
        await session.refresh(new_link)
        new_link.link = f"{link_prefix}{new_link.id}"
        await session.commit()
        return new_link.link

    # если ошибка, то откатываем бд
    except IntegrityError as e:
        await session.rollback()
        if "name" in str(e.orig):
            return "name"
        return None


async def get_all_cities(session: AsyncSession):

    """
    Получаем все города и их chat_id из базы данных.
    Старое решение

    :param session: бд сессия
    :return: словарь, где ключ - chat_id, а значение - название города
    """

    # просто берем все города и chat_id, возвращаем как словарь
    result = await session.execute(select(Channel.chat_id, Channel.city))
    return dict(result.all())


async def get_city_by_chat_id(session: AsyncSession, chat_id: int):

    """

    Получаем информацию о городе по chat_id канала.

    :param session: бд сессия
    :param chat_id: id канала
    :return: объект Channel с данными о городе или None, если не найдено
    """

    # просто достаем весь Channel по его id, возвращаем как есть
    result = await session.execute(select(Channel).where(Channel.chat_id == chat_id))
    return result.scalar()


async def get_city_by_name(session: AsyncSession, city_name: str):

    """
    Получаем информацию о городе по названию.

    :param session: бд сессия
    :param city_name: название города
    :return: объект Channel с данными о городе или None, если не найдено
    """

    # просто получаем Channel, только по city_name, возвращаем как есть
    result = await session.execute(select(Channel).where(Channel.city == city_name))
    return result.scalar()


async def get_platforms(session: AsyncSession):

    """
    Получаем список всех платформ.
    Старое решение, костыльное

    :param session: бд сессия
    :return: словарь, где ключ - индекс платформы (начиная с 1), а значение - название платформы
    """

    # получаем все платформы из бд
    result = await session.execute(select(Platform))

    # преобразуем с индексами для идентификации
    platforms = result.scalars().all()
    return {i + 1: p.platform_name for i, p in enumerate(platforms)}


async def get_platform(session: AsyncSession, rowid: int):
    """
    Получаем информацию о платформе по индексу.
    Старое костыльное решение

    :param session: бд сессия
    :param rowid: индекс платформы в базе данных
    :return: название платформы
    """

    # достаем название платформы по rowid
    result = await session.execute(select(Platform.platform_name).offset(rowid - 1).limit(1))
    return result.scalar()


async def get_link_by_id(session: AsyncSession, link_id: int):

    """
    Получаем ссылку по её ID.

    :param session: бд сессия
    :param link_id: уникальный auto increase id в бд
    :return: объект Link с данными о ссылке или None, если не найдено
    """

    # достаем весь Link по id, возвращаем как есть
    result = await session.execute(select(Link).where(Link.id == link_id))
    return result.scalar()


async def get_city_link(session: AsyncSession, city: str):
    """
    Получаем пригласительную ссылку для города (канала)
    Решение старое, можно было переписать

    :param session: бд сессия
    :param city: название города
    :return: ссылка на канал города или None, если не найдено
    """

    # в бд ищем город, достаем из него пригласительную ссылку и возвращаем
    result = await session.execute(select(Channel.invite_link).where(Channel.city == city))
    return result.scalar()


async def update_user_city(session: AsyncSession, user_id: int, city: str):

    """
    Обновляем город у пользователя по его ID.

    :param session: бд сессия
    :param user_id: id пользователя
    :param city: новый город
    :return: None
    """

    # Получаем пользователя
    user = await get_user(session, user_id)

    if user:
        # Мы хотим обновить значение поля `city` для этого пользователя
        await session.execute(
            update(User)
            .where(User.user_id == user_id)  # Сравниваем user_id с переданным
            .values(city=city)  # Обновляем поле `city`
        )

        await session.commit()  # Подтверждаем изменения


async def get_city_links_stat(session: AsyncSession, city_name: str):

    """
    Получаем статистику по ссылкам для определённого города.

    :param session: бд сессия
    :param city_name: название города
    :return: список объектов Link, относящихся к данному городу
    """

    # достаем Link по city_name, возвращаем все
    result = await session.execute(select(Link).where(Link.city == city_name))
    return result.scalars().all()


async def add_user_to_link(session: AsyncSession, user_id: int, link_str: str):

    """
    Добавляем пользователя в ссылку.
    Именно кто подписался (его id) к ссылке, как счетчик

    Решение старое, можно организовать лучше, под sqlite заходило норм

    :param session: бд сессия
    :param user_id: идентификатор пользователя
    :param link_str: сама ссылка
    :return: None
    """

    # достаем саму ссылку
    result = await session.execute(select(Link).where(Link.link == link_str))
    link_obj = result.scalar()

    if link_obj:

        # если пользователей нет, то добавляем
        if not link_obj.users:
            link_obj.users = str(user_id)

        # если есть, то с новой строки добавляем id
        else:
            users = link_obj.users.split('\n')
            users.append(str(user_id))
            link_obj.users = '\n'.join(users)

        # делаем комит
        await session.commit()


async def get_city_by_channel_id(session: AsyncSession, channel_id: int):

    """
    Получаем объект города / канала по channel_id канала.

    :param session: бд сессия
    :param channel_id: идентификатор канала
    :return: объект Channel с данными о городе или None, если не найдено
    """

    # просто достаем Channel по id, возвращаем как есть
    result = await session.execute(select(Channel).where(Channel.chat_id == channel_id))
    return result.scalar()


# это функции на будущее были, но логика для них еще не прописалась
async def update_user_subscription_do_sub(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user:
        user.subscription = 1
        await session.commit()


async def update_user_subscription_undo_sub(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user:
        user.subscription = 0
        await session.commit()
