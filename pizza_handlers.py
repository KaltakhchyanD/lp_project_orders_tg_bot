from glob import glob
import re, os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters

pizza_main_menu_markup = ReplyKeyboardMarkup([['Menu_button'],
                                              ['Special_offers'],
                                              ['Checkout'],
                                              ['Contact_info']])

from settings import ADMIN_ID, ADMIN_EMAIL
from utils import send_mail
from utils import (add_customer, add_order, get_customer_by_phone,
    get_pizza_by_id, get_pizza_by_name, get_product_by_name)


def pizza_main_menu_handler(bot, update, user_data):
    update.message.reply_text(
        'Добро пожаловать в Орехово Пицца!\nДля просмотра меню, акций\n'+
        'корзины или контактной информации\nнажмите соотвествующую кнопку:',
        reply_markup=pizza_main_menu_markup)
    if 'cart' not in user_data.keys():
        user_data['cart']=[]
    return 'pizzeria_main_menu_state'


def menu_button_handler(bot, update, user_data):
    update.message.reply_text('Выберите категорию или вернитесь назад:',
                              reply_markup=ReplyKeyboardMarkup([['Пицца'],
                                                                ['Напитки'],
                                                                ['Прочее'],
                                                                ['Назад']]))
    user_data['pizza'] = {'menu_page':0}
    return 'pizzeria_menu_state'

pizza_names_dict = {}

def print_pizza_menu(bot, update, user_data):
    pizza_num = user_data['pizza']['menu_page']
    optional_buttons = [['Пред.', 'След.', 'Назад']]
    if not pizza_num:
        optional_buttons[0].pop(0)
    elif pizza_num == 2:
        optional_buttons[0].pop(1)
    if not len(pizza_names_dict):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        pizza_photos = glob(current_dir+'/images/pizza/pizza*.jp*g')
        for i in pizza_photos:
            k = re.search(r'pizza(\d+)\.j', i)
            pizza_names_dict[k.group(1)] = i

    markup = [[get_pizza_by_id(i + 1).name] for i in range(pizza_num * 5, min(5 + pizza_num * 5, 11))] + optional_buttons

    for i in range(pizza_num * 5, min(5 + pizza_num * 5, 11)):  # 2nd value in min() should be fixed!
        with open(pizza_names_dict[str(i+1)], 'rb') as f:
            bot.send_photo(chat_id=update.message.chat.id, photo=f)
    update.message.reply_text('Выберите пиццу:', reply_markup=ReplyKeyboardMarkup(markup, resize_keyboard=True))


def pizza_category_handler(bot, update, user_data):
    print_pizza_menu(bot, update, user_data)
    return 'pizza_choise_state'


def add_pizza_to_cart_handler(bot, update, user_data):
    pizza_name = update.message.text
    user_data['cart'].append(get_pizza_by_name(pizza_name))
    update.message.reply_text(f'Пицца {pizza_name} добавлена в корзину')


def change_menu_page_handler(bot, update, user_data):
    if update.message.text == 'Пред.':
        user_data['pizza']['menu_page'] -= 1
        print_pizza_menu(bot, update, user_data)
    elif update.message.text == 'След.':
        user_data['pizza']['menu_page'] += 1
        print_pizza_menu(bot, update, user_data)
    elif update.message.text == 'Назад':
        return menu_button_handler(bot, update, user_data)


def checkout_handler(bot, update, user_data):
    user_id =  update.message.from_user['id']
    cart = user_data['cart']
    if not len(cart):
        update.message.reply_text('Ваша корзина пуста', reply_markup=ReplyKeyboardMarkup([['Назад']]))
    else:
        product_names = [i.name for i in cart]
        for i in sorted(set(product_names)):
            update.message.reply_text(f'{i} x{product_names.count(i)}, Цена: {get_product_by_name(i).price}\n')
        update.message.reply_text('Для изменения заказа, нажмите соотвествующую кнопку', 
            reply_markup = ReplyKeyboardMarkup([['Изменить заказ'],['Назад'],['Сделать заказ']]))
    return 'pizzeria_checkout_state'


def change_cart_handler(bot, update, user_data):
    user_id =  update.message.from_user['id']
    cart = user_data['cart']
    product_names = [i.name for i in cart]
    markup = [[f'{i} x{product_names.count(i)} -1'] for i in sorted(set(product_names))]
    markup.extend([['Назад']])
    update.message.reply_text('Для уменьшения колличества позиций на 1\n'+
        'нажмите соотвествующую кнопку',
        reply_markup = ReplyKeyboardMarkup(markup, resize_keyboard=True))
    return 'removing_from_cart_state'


def remove_from_cart_handler(bot, update, user_data):
    item = re.search(r'(\w+)x\w\s*-1', update.message.text).group(1)
    user_id = update.message.from_user['id']
    cart = user_data['cart']
    cart.remove(item)
    return change_cart_handler(bot, update, user_data)


def order_pizza_handler(bot, update, user_data):
    user_id =  update.message.from_user['id']
    cart = user_data['cart']
    update.message.reply_text('Ваш заказ:',
        reply_markup = ReplyKeyboardMarkup([['Назад'],['Отправить заказ']]))
    product_names = [i.name for i in cart]
    for i in sorted(set(product_names)):
        update.message.reply_text(f'{i} x{product_names.count(i)}, Цена: {get_pizza_by_name(i).price}\n')
    return 'pizzeria_make_order_state'


def send_order_handler(bot, update, user_data):
    user_id =  update.message.from_user['id']
    if not get_customer_by_phone(user_data['phone']):
        add_customer(user_data['name'], user_data['phone'], user_id)
    add_order('some text', get_customer_by_phone(user_data['phone']).id, *user_data["cart"])
    msg = f'Пользователь {user_id} сделал заказ:\n'+f'{user_data["cart"]}'
    bot.send_message(ADMIN_ID, msg)
    send_mail(msg, ADMIN_EMAIL)
    update.message.reply_text('Спасибо за заказ, вам позвонит оператор')
    return pizza_main_menu_handler(bot, update, user_data)


# Dummy handlers to test conversation handler
def special_offers_handler(bot, update, user_data):
    update.message.reply_text('This is special offers button')
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

# def
