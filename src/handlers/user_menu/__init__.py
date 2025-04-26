# импорт самого роутера
from .user_menu_router import user_menu_router

# импорт хендлеров из главного меню юзера
from src.handlers.user_menu.main.make_order import *
from src.handlers.user_menu.main.delivery import *
from src.handlers.user_menu.main.pay_order import *
from src.handlers.user_menu.main.about_us import *
from src.handlers.user_menu.main.main_menu import *

# импорт хендлеров из FAQ меню юзера
from src.handlers.user_menu.faq.faq import *
from src.handlers.user_menu.faq.where_price import *
from src.handlers.user_menu.faq.where_receive import *
from src.handlers.user_menu.faq.min_weigh import *
from src.handlers.user_menu.faq.order_schedule import *
from src.handlers.user_menu.faq.call_manager import *

# импорт команд старт и смены города
from src.handlers.user_menu.command_start import *
from src.handlers.user_menu.command_start_link import *
from src.handlers.user_menu.change_city import *
