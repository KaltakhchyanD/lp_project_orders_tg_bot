import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters

from pizza_handlers import (pizza_main_menu_handler, menu_button_handler, special_offers_handler,
                            checkout_handler, contact_info_handler, pizza_category_handler, drinks_category_handler,
                            other_category_handler, back_from_menu_handler, add_pizza_to_cart_handler,
                            change_menu_page_handler, back_from_checkout_handler, change_cart_handler,
                            order_pizza_handler, back_from_order_handler, send_order_handler, 
                            remove_from_cart_handler, back_from_removing_from_cart_handler
                            )


def start_handler(bot, update, user_data):
    update.message.reply_text('Привет, я бот, который поможет\nтебе заказать пиццу или выпить кофе!\n'+
        'Выбери опцию, нажав одну из кнопок:', reply_markup=ReplyKeyboardMarkup([
            ['Pizza main menu'], ['Cafe main menu']]))
    return 'mode_choise_state'


def cafe_main_menu_handler(bot, update, user_data):
    update.message.reply_text('Here will be cafe menu', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def end_handler(bot, update, user_data):
    update.message.reply_text('End state!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel_handler(bot, update, user_data):
    update.message.reply_text('You have canceled the conversation', reply_markup=ReplyKeyboardRemove())


def enter_name_and_phone_handler(bot, update, user_data):
    phone_button = KeyboardButton('Телефон', request_contact=True)
    update.message.reply_text('Пожалуйста, заполните данные о себе:',
        reply_markup=ReplyKeyboardMarkup([[phone_button], ['Ввести имя'],['Назад']]))
    return 'enter_phone_choise'


def enter_phone_handler(bot, update, user_data):
    if 'phone' in user_data.keys():
        update.message.reply_text(f'Я знаю, что ваш Телефон - {user_data["phone"]}')
        return enter_name_and_phone_handler(bot, update, user_data)
    else:
        update.message.reply_text(f'Ваш Телефон - {update.message.contact["phone_number"]}?',
                                  reply_markup=ReplyKeyboardMarkup([['Yes'], ['No']]))
        user_data['temp'] = update.message.contact['phone_number']
    return 'phone_choise'


def phone_good_handler(bot, update, user_data):
    user_data['phone'] = user_data['temp']
    update.message.reply_text(f'Отлично, я запомню его {user_data["phone"]}')
    return check_user_data_completeness(bot, update, user_data)


def phone_bad_handler(bot, update, user_data):
    update.message.reply_text('Тогда введите его в формате 79001234567:')
    return 'phone_input'


def check_phone_input_handler(bot, update, user_data):
    user_input = update.message.text.lstrip().rstrip()
    print(user_input)
    phone_to_check = re.findall(r'^\d{11}$', user_input)
    print(phone_to_check)
    if len(phone_to_check) != 1:
        update.message.reply_text('Проверьте формат ввода и введие снова')
        return 'phone_input'
    else:
        user_data['phone'] = user_input
        update.message.reply_text(f'Отлично, я запомню его {user_data["phone"]}')
        return enter_name_and_phone_handler(bot, update, user_data)


def enter_name_handler(bot, update, user_data):
    if 'name' in user_data.keys():
        update.message.reply_text(f'Я знаю, что вас зовут - {user_data["name"]}')
        return enter_name_and_phone_handler(bot, update, user_data)
    else:
        update.message.reply_text(f'Вас зовут - {update.message.from_user.full_name}?',
                                  reply_markup=ReplyKeyboardMarkup([['Yes'], ['No']]))
    return 'name_choise'


def name_good_handler(bot, update, user_data):
    user_data['name'] = update.message.from_user.full_name
    update.message.reply_text(f'Отлично, я запомню его {user_data["name"]}')
    return check_user_data_completeness(bot, update, user_data)


def name_bad_handler(bot, update, user_data):
    update.message.reply_text('Тогда введите его в формате Имя Фамилия:')
    return 'name_input'


def check_name_input_handler(bot, update, user_data):
    user_input = update.message.text.lstrip().rstrip()
    print(user_input)
    name_to_check = re.findall(r'\w+ \w+', user_input)  # TODO - replace \w with smth
    print(name_to_check)
    if len(name_to_check) != 1:
        update.message.reply_text('Проверьте формат ввода и введие снова')
        return 'name_input'
    else:
        user_data['name'] = user_input
        update.message.reply_text(f'Отлично, я запомню его {user_data["name"]}')
        return enter_name_and_phone_handler(bot, update, user_data)


def check_user_data_completeness(bot, update, user_data):
    if 'phone' in user_data.keys() and 'name' in user_data.keys():
        return 'pizzeria_send_order'
    else:
        return enter_name_and_phone_handler(bot, update, user_data)


conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler, pass_user_data=True)],
    states={
        'mode_choise_state': [
            RegexHandler('^(Pizza main menu)$', pizza_main_menu_handler, pass_user_data=True),
            RegexHandler('^(Cafe main menu)$', cafe_main_menu_handler, pass_user_data=True),
            RegexHandler('^(enter_phone_and_name)$', enter_name_and_phone_handler, pass_user_data=True)
        ],

        'pizzeria_main_menu_state': [
            RegexHandler('^(Menu_button)$', menu_button_handler, pass_user_data=True),
            RegexHandler('^(Special_offers)$', special_offers_handler, pass_user_data=True),
            RegexHandler('^(Checkout)$', checkout_handler, pass_user_data=True),
            RegexHandler('^(Contact_info)$', contact_info_handler, pass_user_data=True)
        ],
        'pizzeria_menu_state': [
            RegexHandler('^(Пицца)$', pizza_category_handler, pass_user_data=True),
            RegexHandler('^(Напитки)$', drinks_category_handler, pass_user_data=True),
            RegexHandler('^(Прочее)$', other_category_handler, pass_user_data=True),
            RegexHandler('^(Назад)$', back_from_menu_handler, pass_user_data=True)
        ],
        'pizza_choise_state': [
            RegexHandler('^\d+$', add_pizza_to_cart_handler, pass_user_data=True),
            RegexHandler('^Пред\.|След\.|Назад$', change_menu_page_handler, pass_user_data=True)
        ],

        'pizzeria_checkout_state':[
            RegexHandler('^(Назад)$', back_from_checkout_handler, pass_user_data=True),
            RegexHandler('^(Изменить заказ)$', change_cart_handler, pass_user_data=True),
            RegexHandler('^Сделать заказ$', order_pizza_handler, pass_user_data=True)
        ],
        'removeing_from_cart_state': [
            RegexHandler('^\w+x\w\s*-1$', remove_from_cart_handler, pass_user_data=True),
            RegexHandler('^(Назад)$', back_from_removing_from_cart_handler, pass_user_data=True),
        ],

        'pizzeria_make_order_state': [
            RegexHandler('^(Назад)$', back_from_order_handler, pass_user_data=True),
            RegexHandler('^(Отправить заказ)$', enter_name_and_phone_handler, pass_user_data=True)
        ],
        'pizzeria_send_order': [
            MessageHandler(Filters.text, send_order_handler, pass_user_data=True)
        ],

        'enter_phone_choise': [
            MessageHandler(Filters.contact, enter_phone_handler, pass_user_data=True),
            RegexHandler('^(Ввести имя)$', enter_name_handler, pass_user_data=True),
            RegexHandler('^(Назад)$', back_from_menu_handler, pass_user_data=True)
        ],
        'phone_choise': [
            RegexHandler('^(Yes)$', phone_good_handler, pass_user_data=True),
            RegexHandler('^(No)$', phone_bad_handler, pass_user_data=True),
        ],
        'phone_input': [
            MessageHandler(Filters.text, check_phone_input_handler, pass_user_data=True)
        ],
        'name_choise': [
            RegexHandler('^(Yes)$', name_good_handler, pass_user_data=True),
            RegexHandler('^(No)$', name_bad_handler, pass_user_data=True),
        ],
        'name_input': [
            MessageHandler(Filters.text, check_name_input_handler, pass_user_data=True)
        ],

        'end': [
            MessageHandler(Filters.text, end_handler, pass_user_data=True)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel_handler, pass_user_data=True)]
)
