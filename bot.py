import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from handlers import conversation
from settings import PROXY
from settings import API_KEY

from cafe_handlers import (cafe_main_menu_handler, keyboard_coffee, keyboard_sweets, send_Americano_description,
    send_Capuccino_description, send_Glase_description, send_Latte_description, send_Kozinka_description,
    send_Sharlotka_description, send_Browny_description, send_HotDog_description, send_Cupcacke_description
)



logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
#                    filename='bot.log'
                    )

logger = logging.getLogger(__name__)
logger.info('BOT-BOT')



def main():
    mybot = Updater(API_KEY, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(conversation)
    dp.add_handler(CommandHandler('coffee', keyboard_coffee)) #, pass_user_data=True))
    dp.add_handler(CommandHandler('sweets', keyboard_sweets)) #, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Hi {})$', emo, pass_user_data=True))
    dp.add_handler(RegexHandler('^(coffee)$', keyboard_coffee)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(на главную)$', cafe_main_menu_handler)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(sweets)$', keyboard_sweets)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(Americano)$', send_Americano_description)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(Capuccino)$', send_Capuccino_description)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Гляссе)$', send_Glase_description)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Latte)$', send_Latte_description)) #, pass_user_data=True))
    dp.add_handler(RegexHandler('^(корзиночку)$', send_Kozinka_description)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(шарлотку)$', send_Sharlotka_description)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(Browny)$', send_Browny_description)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(hot dog)$', send_HotDog_description)) # , pass_user_data=True))
    dp.add_handler(RegexHandler('^(chocupcake)$', send_Cupcacke_description)) # , pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()