from glob import glob
import re

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
    user_data['pizza'] = {}
    user_data['pizza']['menu_page'] = 0
    return 'menu_state'


def back_from_menu_handler(bot, update, user_data): 
    update.message.reply_text(
    '''Для просмотра меню, акций,\nкорзины или контактной информации
нажмите соотвествующую кнопку:''',
    reply_markup = pizza_main_menu_markup)
    return 'state_choise'


def print_pizza_menu(bot, update, user_data):
    pizza_photos = glob('images/pizza/pizza*.jp*g')
    dct ={}
    for i in pizza_photos:
        k = re.search(r'pizza(\d+)\.j',i)
        dct[k.group(1)]=i
    pizza_num = user_data['pizza']['menu_page']
    optional_buttons = [['Пред.','След.','Назад']]
    if not pizza_num:
        optional_buttons[0].pop(0)
    elif pizza_num == 2:
        optional_buttons[0].pop(1)
        
    markup = [[str(i+1)] for i in range(pizza_num*5, min(5+pizza_num*5,14))]+optional_buttons
    for i in range(pizza_num*5, min(5+pizza_num*5,14)):
        with open(dct[str(i)], 'rb') as f:
            bot.send_photo(chat_id=update.message.chat.id, photo=f)
    update.message.reply_text('Выберите пиццу:', reply_markup = ReplyKeyboardMarkup(markup, resize_keyboard=True))


def pizza_category_handler(bot, update, user_data):
    print_pizza_menu(bot, update, user_data)
    update.message.reply_text('Здесь будет выбор пиццы')
    return 'pizza_choise'


def add_pizza_to_order_handler(bot, update, user_data):
    pizza_index = update.message.text
    update.message.reply_text(f'Пицца №{pizza_index} добавленя в корзину')
    print_pizza_menu(bot, update, user_data)


def change_menu_page_handler(bot, update, user_data):
    if update.message.text == 'Пред.':
        user_data['pizza']['menu_page']-=1
        print_pizza_menu(bot, update, user_data)
    elif update.message.text == 'След.':
        user_data['pizza']['menu_page']+=1
        print_pizza_menu(bot, update, user_data)
    elif update.message.text == 'Назад':
        menu_button_handler(bot, update, user_data)
        return 'menu_state'


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


def drinks_category_handler(bot, update, user_data):
    update.message.reply_text('Здесь будет выбор напитков')
    return 'end'


def other_category_handler(bot, update, user_data):
    update.message.reply_text('Здесь будет прочее')
    return 'end'


#def 
