from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters

from pizza_handlers import (pizza_main_menu_handler, menu_button_handler, special_offers_handler,
    checkout_handler, contact_info_handler, pizza_category_handler, drinks_category_handler,
    other_category_handler, back_from_menu_handler
)


def start_handler(bot, update, user_data):
    update.message.reply_text(''' Привет, я бот, который поможет
тебе заказать пиццу или выпить кофе!
Выбери опцию, нажав одну из кнопок:''',
         reply_markup = ReplyKeyboardMarkup([['Pizza main menu'],['Cafe main menu']]))
    return 'mode_choise_state'


def cafe_main_menu_handler(bot, update, user_data):
    update.message.reply_text('Here will be cafe menu', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def end_handler(bot, update, user_data):
    update.message.reply_text('End state!', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END 


def cancel_handler(bot, update, user_data):
    update.message.reply_text('You have canceled the conversation', reply_markup = ReplyKeyboardRemove()) 


conversation = ConversationHandler(
    entry_points = [CommandHandler('start', start_handler, pass_user_data = True)],
    states = {
        'mode_choise_state':[
            RegexHandler('^(Pizza main menu)$', pizza_main_menu_handler, pass_user_data = True),
            RegexHandler('^(Cafe main menu)$', cafe_main_menu_handler, pass_user_data = True),
        ],
        'state_choise':[
            RegexHandler('^(Menu_button)$', menu_button_handler, pass_user_data = True),
            RegexHandler('^(Special_offers)$', special_offers_handler, pass_user_data = True),
            RegexHandler('^(Checkout)$', checkout_handler, pass_user_data = True),
            RegexHandler('^(Contact_info)$', contact_info_handler, pass_user_data = True)
            ],
        'menu_state':[
            RegexHandler('^(Пицца)$', pizza_category_handler, pass_user_data = True),
            RegexHandler('^(Напитки)$', drinks_category_handler, pass_user_data = True),
            RegexHandler('^(Прочее)$', other_category_handler, pass_user_data = True),
            RegexHandler('^(Назад)$', back_from_menu_handler, pass_user_data = True)
        ],
        'end' :[MessageHandler(Filters.text, end_handler, pass_user_data = True)]
        },

    fallbacks = [CommandHandler('cancel', cancel_handler, pass_user_data = True)]
    )



