from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters


pizza_main_menu_markup = ReplyKeyboardMarkup([['Menu_button'],
                                     ['Special_offers'],
                                     ['Checkout'],
                                     ['Contact_info']]) 


def pizza_main_menu_handler(bot, update, user_data):
    update.message.reply_text(
    '''Добро пожаловать в Орехово Пицца!\nДля просмотра меню, акций,
корзины или контактной информации\nнажмите соотвествующую кнопку:''',
    reply_markup = pizza_main_menu_markup)
    return 'state_choise'


def menu_button_handler(bot, update, user_data):
    update.message.reply_text('Выберите категорию или вернитесь назад:',
        reply_markup = ReplyKeyboardMarkup([['Пицца'],['Напитки'],['Прочее'],['Назад']]))
    return 'menu_state'


def back_from_menu_handler(bot, update, user_data): 
    update.message.reply_text(
    '''Для просмотра меню, акций,\nкорзины или контактной информации
нажмите соотвествующую кнопку:''',
    reply_markup = pizza_main_menu_markup)
    return 'state_choise'


# Dummy handlers to test conversation handler
def special_offers_handler(bot, update, user_data):
    update.message.reply_text('This is special offers button')
    return 'end'


def checkout_handler(bot, update, user_data):
    update.message.reply_text('This is checkout button')
    return 'end'


def contact_info_handler(bot, update, user_data):
    update.message.reply_text('This is contact info button')
    return 'end'


def pizza_category_handler(bot, update, user_data):
    update.message.reply_text('Здесь будет выбор пиццы')
    return 'end'


def drinks_category_handler(bot, update, user_data):
    update.message.reply_text('Здесь будет выбор напитков')
    return 'end'


def other_category_handler(bot, update, user_data):
    update.message.reply_text('Здесь будет прочее')
    return 'end'

