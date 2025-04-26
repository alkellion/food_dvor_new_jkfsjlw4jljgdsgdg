from src.handlers.user_menu.user_menu_router import user_menu_router
from src.handlers.admin_menu.admin_menu_router import admin_menu_router
from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router


# импортируем все роутеры и закидываем в один кортеж
routers = (
    user_menu_router,
    admin_menu_router,
    links_menu_router,
    )


