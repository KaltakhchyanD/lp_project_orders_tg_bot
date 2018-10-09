import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters

from pizza_handlers import (pizza_main_menu_handler, menu_button_handler, special_offers_handler,
    checkout_handler, contact_info_handler, pizza_category_handler, drinks_category_handler,
    other_category_handler, back_from_menu_handler
)

from cafe_handlers import (cafe_main_menu_handler, keyboard_coffee, keyboard_sweets, 
    send_HotDog_description, send_Americano_description,
    send_Capuccino_description, send_Glase_description, send_Latte_description, send_Kozinka_description,
    send_Sharlotka_description, send_Browny_description, send_Cupcacke_description
)


def start_handler(bot, update, user_data):
    update.message.reply_text(''' Привет, я бот, который поможет
тебе заказать пиццу или  кофеёк с плюшками!
Выбери опцию, нажав одну из кнопок:''',
         reply_markup = ReplyKeyboardMarkup([['Pizza main menu'],['Cafe main menu'],['Test_phone_and_name']]))
    return 'mode_choise_state'



def end_handler(bot, update, user_data):
    update.message.reply_text('End state!', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END 


def show_my_basket(bot, update, user_data):
    update.message.reply_text('Пока корзина не готова, сорри!', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END 


def cancel_handler(bot, update, user_data):
    update.message.reply_text('You have canceled the conversation', reply_markup = ReplyKeyboardRemove()) 


def test_name_and_phone(bot, update, user_data):
    phone_button = KeyboardButton('Телефон', request_contact = True)
    update.message.reply_text('Выберите опцию:',reply_markup = ReplyKeyboardMarkup([[phone_button],['Ввести имя']]))
    return 'test_phone_choise'


def test_phone(bot, update, user_data):
    if 'phone' in user_data.keys():
        update.message.reply_text(f'Я знаю, что ваш Телефон - {user_data["phone"]}')
        return ConversationHandler.END
    else:
        update.message.reply_text(f'Ваш Телефон - {update.message.contact["phone_number"]}?',reply_markup = ReplyKeyboardMarkup([['Yes'],['No']]))
        user_data['temp'] = update.message.contact['phone_number']
    return 'phone_choise'


def phone_good(bot, update, user_data):
    user_data['phone'] = user_data['temp']
    update.message.reply_text(f'Отлично, я запомню его {user_data["phone"]}')
    return ConversationHandler.END


def phone_bad(bot, update, user_data):
    update.message.reply_text('Тогда введите его в формате 79001234567:')
    return 'phone_input'


def check_phone_input(bot, update, user_data):
    user_input = update.message.text.lstrip().rstrip()
    print(user_input)
    phone_to_check = re.findall(r'\d{11}',user_input)
    print(phone_to_check)
    if len(phone_to_check)!=1:
        update.message.reply_text('Проверьте формат ввода и введие снова')
        return 'phone_input'
    else:
        user_data['phone'] = user_input
        update.message.reply_text(f'Отлично, я запомню его {user_data["phone"]}')
        return ConversationHandler.END


def test_name(bot, update, user_data):
    if 'name' in user_data.keys():
        update.message.reply_text(f'Я знаю, что вас зовут - {user_data["name"]}')
        return ConversationHandler.END
    else:
        update.message.reply_text(f'Вас зовут - {update.message.from_user.full_name}?',reply_markup = ReplyKeyboardMarkup([['Yes'],['No']]))
#        user_data['temp'] = update.message.contact['phone_number']
    return 'name_choise'


def name_good(bot, update, user_data):
    user_data['name'] = update.message.from_user.full_name
    update.message.reply_text(f'Отлично, я запомню его {user_data["name"]}')
    return ConversationHandler.END


def name_bad(bot, update, user_data):
    update.message.reply_text('Тогда введите его в формате Имя Фамилия:')
    return 'name_input'


def check_name_input(bot, update, user_data):
    user_input = update.message.text.lstrip().rstrip()
    print(user_input)
    name_to_check = re.findall(r'\w+ \w+',user_input)       #TODO - replace \w with smth
    print(name_to_check)
    if len(name_to_check)!=1:
        update.message.reply_text('Проверьте формат ввода и введие снова')
        return 'name_input'
    else:
        user_data['name'] = user_input
        update.message.reply_text(f'Отлично, я запомню его {user_data["name"]}')
        return ConversationHandler.END




conversation = ConversationHandler(
    entry_points = [CommandHandler('start', start_handler, pass_user_data = True)],
    states = {
        'mode_choise_state':[
            RegexHandler('^(Pizza main menu)$', pizza_main_menu_handler, pass_user_data = True),
            RegexHandler('^(Cafe main menu)$', cafe_main_menu_handler, pass_user_data = True),
            RegexHandler('^(Test_phone_and_name)$', test_name_and_phone, pass_user_data = True)
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
        'menu_cafe_state':[
            RegexHandler('^(Menu_coffee)$', keyboard_coffee, pass_user_data = True),
            RegexHandler('^(Menu_sweets)$', keyboard_sweets, pass_user_data = True),
            RegexHandler('^(Прочее)$', other_category_handler, pass_user_data = True),
            RegexHandler('^(Назад)$', back_from_menu_handler, pass_user_data = True)
        ],
        'menu_coffee_bar':[
            RegexHandler('^(В начало)$', start_handler, pass_user_data = True),
            RegexHandler('^(Menu_sweets)$', keyboard_sweets, pass_user_data = True),
            RegexHandler('^(корзина)$', show_my_basket, pass_user_data = True),
            RegexHandler('^(Americano)$', send_Americano_description, pass_user_data = True),
            RegexHandler('^(Capuccino)$', send_Capuccino_description, pass_user_data=True),
            RegexHandler('^(Гляссе)$', send_Glase_description, pass_user_data=True),
            RegexHandler('^(Latte)$', send_Latte_description, pass_user_data=True)
        ],
        'menu_sweets_bar':[
            RegexHandler('^(В начало)$', start_handler, pass_user_data = True),
            RegexHandler('^(menu_coffee_bar)$', keyboard_coffee, pass_user_data = True),
            RegexHandler('^(корзина)$', show_my_basket, pass_user_data = True),
            RegexHandler('^(корзиночку)$', send_Kozinka_description, pass_user_data = True),
            RegexHandler('^(шарлотку)$', send_Sharlotka_description, pass_user_data = True),
            RegexHandler('^(Browny)$', send_Browny_description, pass_user_data=True),
            RegexHandler('^(hot dog)$', send_HotDog_description, pass_user_data=True),
            RegexHandler('^(chocupcake)$', send_Cupcacke_description, pass_user_data=True)
        ], 
        'test_phone_choise':[
            MessageHandler(Filters.contact, test_phone, pass_user_data=True),
            RegexHandler('^(Ввести имя)$', test_name, pass_user_data = True)
        ],
        'phone_choise':[
            RegexHandler('^(Yes)$', phone_good, pass_user_data=True),
            RegexHandler('^(No)$', phone_bad, pass_user_data=True),
            RegexHandler('^(В начало)$', start_handler, pass_user_data = True),
        ],
        'phone_input':[
            MessageHandler(Filters.text, check_phone_input, pass_user_data = True)
        ],
      
        'name_choise':[
            RegexHandler('^(Yes)$', name_good, pass_user_data=True),
            RegexHandler('^(No)$', name_bad, pass_user_data=True),
            RegexHandler('^(В начало)$', start_handler, pass_user_data = True),
        ],        
        'name_input':[
            MessageHandler(Filters.text, check_name_input, pass_user_data = True)
        ],  
        'end' :[
        MessageHandler(Filters.text, end_handler, pass_user_data = True)
        ]
    },

    fallbacks = [CommandHandler('cancel', cancel_handler, pass_user_data = True)]
    )



