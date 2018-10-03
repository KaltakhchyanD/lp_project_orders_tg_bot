from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters




def start_handler(bot, update, user_data):
    update.message.reply_text('Hello!', reply_markup = ReplyKeyboardRemove())


def pizza_main_menu_handler(bot, update, user_data):
    kb_markup = ReplyKeyboardMarkup([['Menu_button'],
                                     ['Special_offers'],
                                     ['Checkout'],
                                     ['Contact_info']])    
    update.message.reply_text(
    '''Добро пожаловать в Орехово Пицца!\nДля просмотра меню, акций,
корзины или контактной информации\nнажмите соотвествующую кнопку:''',
    reply_markup = kb_markup)
    return 'state_choise'


# Dummy handlers to test conversation handler
def menu_button_handler(bot, update, user_data):
    update.message.reply_text('This is menu button')
    return 'end'


def special_offers_handler(bot, update, user_data):
    update.message.reply_text('This is special offers button')
    return 'end'


def checkout_handler(bot, update, user_data):
    update.message.reply_text('This is checkout button')
    return 'end'


def contact_info_handler(bot, update, user_data):
    update.message.reply_text('This is contact info button')
    return 'end'


def end_handler(bot, update, user_data):
    update.message.reply_text('End state!', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END 


def cancel_handler(bot, update, user_data):
    update.message.reply_text('You have canceled the conversation', reply_markup = ReplyKeyboardRemove()) 


pizza_main_menu = ConversationHandler(
    entry_points = [RegexHandler('^(Pizza main menu)$', pizza_main_menu_handler, pass_user_data = True)],
    states = {
        'state_choise':[
            RegexHandler('^(Menu_button)$', menu_button_handler, pass_user_data = True),
            RegexHandler('^(Special_offers)$', special_offers_handler, pass_user_data = True),
            RegexHandler('^(Checkout)$', checkout_handler, pass_user_data = True),
            RegexHandler('^(Contact_info)$', contact_info_handler, pass_user_data = True)
            ],
        'end' :[MessageHandler(Filters.text, end_handler, pass_user_data = True)]
        },

    fallbacks = [CommandHandler('cancel', cancel_handler, pass_user_data = True)]
    )

