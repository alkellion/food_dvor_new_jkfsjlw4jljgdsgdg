from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.context import FSMContext
from logs.logger_config import logger

from datetime import datetime, timedelta
from typing import Callable, Dict, Any, Awaitable
import asyncio


class InactivityMiddleware(BaseMiddleware):
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.last_activity: Dict[int, datetime] = {}
        self.tasks: Dict[int, asyncio.Task] = {}  # ключ - user_id, значение - asyncio.Task

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        if not user:
            return await handler(event, data)

        user_id = user.id
        now = datetime.now()
        self.last_activity[user_id] = now

        # Если уже есть запущенный таймер — отменим его
        old_task = self.tasks.get(user_id)
        if old_task and not old_task.done():
            old_task.cancel()

        # Запускаем новый таймер
        state: FSMContext = data["state"]
        self.tasks[user_id] = asyncio.create_task(self._check_inactivity(user_id, state))

        return await handler(event, data)

    async def _check_inactivity(self, user_id: int, state: FSMContext):
        current_task = asyncio.current_task()

        # Обновляем текущую задачу
        self.tasks[user_id] = current_task

        try:
            await asyncio.sleep(self.timeout)
            last = self.last_activity.get(user_id)

            if last and datetime.now() - last > timedelta(seconds=self.timeout):
                await state.clear()
                self.last_activity.pop(user_id, None)

        except asyncio.CancelledError:
            pass

        finally:
            # Удаляем задачу, если она всё ещё актуальна (а не уже перезапущена)
            if self.tasks.get(user_id) is current_task:
                await self.tasks.pop(user_id, None)
