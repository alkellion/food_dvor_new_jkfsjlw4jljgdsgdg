# импорт самого роутера
from .links_menu_router import links_menu_router

# импорт модуля меню ссылок из меню ссылок
from src.handlers.admin_menu.links_menu.links_menu import *

# импорт модулей из меню ссылок -> создание ссылки
from src.handlers.admin_menu.links_menu.create_link.create_link_menu import *
from src.handlers.admin_menu.links_menu.create_link.add_link_name import *
from src.handlers.admin_menu.links_menu.create_link.add_link_city import *
from src.handlers.admin_menu.links_menu.create_link.add_link_platform import *
from src.handlers.admin_menu.links_menu.create_link.set_link import *

# импорт модулей из меню статистика ссылок
from src.handlers.admin_menu.links_menu.links_stat.links_stat_menu import *
