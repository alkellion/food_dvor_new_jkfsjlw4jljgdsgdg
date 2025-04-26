from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update, values
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Link, Channel, Platform


async def add_user(session: AsyncSession, user_id: int, join_link, city, platform):
    join_date = datetime.now()

    new_user = User(user_id=user_id,
                    ban=0,
                    join_link=join_link,
                    join_date=join_date,
                    city=city,
                    platform=platform)
    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()


async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar()


async def db_create_link(session: AsyncSession, name, city, platform, link_prefix):
    date = datetime.now(timezone(timedelta(hours=3))).isoformat()
    new_link = Link(name=name, city=city, platform=platform, date=date)
    session.add(new_link)

    try:
        await session.commit()
        await session.refresh(new_link)
        new_link.link = f"{link_prefix}{new_link.id}"
        await session.commit()
        return new_link.link

    except IntegrityError as e:
        await session.rollback()
        if "name" in str(e.orig):
            return "name"
        return None


async def get_all_cities(session: AsyncSession):
    result = await session.execute(select(Channel.chat_id, Channel.city))
    return dict(result.all())


async def get_city_by_chat_id(session: AsyncSession, chat_id: int):

    """

    :param session:
    :param chat_id:
    :return:
    """

    result = await session.execute(select(Channel).where(Channel.chat_id == chat_id))
    return result.scalar()


async def get_city_by_name(session: AsyncSession, city_name: str):

    """

    :param session:
    :param city_name:
    :return:
    """

    result = await session.execute(select(Channel).where(Channel.city == city_name))
    return result.scalar()


async def get_platforms(session: AsyncSession):
    result = await session.execute(select(Platform))
    platforms = result.scalars().all()
    return {i + 1: p.platform_name for i, p in enumerate(platforms)}


async def get_platform(session: AsyncSession, rowid: int):
    result = await session.execute(select(Platform.platform_name).offset(rowid - 1).limit(1))
    return result.scalar()


async def get_link_by_id(session: AsyncSession, link_id: int):
    result = await session.execute(select(Link).where(Link.id == link_id))
    return result.scalar()


async def get_city_link(session: AsyncSession, city: str):
    result = await session.execute(select(Channel.invite_link).where(Channel.city == city))
    return result.scalar()


async def update_user_city(session: AsyncSession, user_id: int, city: str):
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
    result = await session.execute(select(Link).where(Link.city == city_name))
    return result.scalars().all()


async def add_user_to_link(session: AsyncSession, user_id, link_str):
    result = await session.execute(select(Link).where(Link.link == link_str))
    link_obj = result.scalar()
    if link_obj:
        if not link_obj.users:
            link_obj.users = str(user_id)
        else:
            users = link_obj.users.split('\n')
            users.append(str(user_id))
            link_obj.users = '\n'.join(users)
        await session.commit()


async def update_user_subscription(session: AsyncSession, user_id: int, status: str):
    user = await get_user(session, user_id)
    if user:
        user.subscription = 1 if status == 'member' else 0
        await session.commit()


async def get_city_by_channel_id(session: AsyncSession, channel_id: int):
    result = await session.execute(select(Channel).where(Channel.chat_id == channel_id))
    return result.scalar()


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
