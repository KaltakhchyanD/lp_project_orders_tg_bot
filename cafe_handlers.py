from emoji import emojize
from glob import glob
import logging
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



def cafe_main_menu_handler(bot, update, user_data):
    text = 'самое меню кафе'
    my_keyboard = ReplyKeyboardMarkup([
                                        ['sweets','coffee'] 
                                       ], resize_keyboard=True
                                      )     
    update.message.reply_text(text, reply_markup=my_keyboard)


def keyboard_coffee(bot, update):
    text = 'Привет, что бы вы хотели из кофе?'    
    my_button = ReplyKeyboardMarkup([
                                        ['на главную','корзина'],
                                        ['Americano','Гляссе' ],
                                        ['Capuccino','Latte']
                                       ], resize_keyboard=True
                                      )
    update.message.reply_text(text, reply_markup = my_button) # удалить скобку и коменты , reply_markup=my_keyboard)


def keyboard_sweets(bot, update):
    # contact_button = KeyboardButton('Пришли контакты', request_contact=True)
    # location_button = KeyboardButton('Пришли локацию', request_location=True)
    text = 'Привет, что бы вы хотели из бейкери, из сладенького?'    
    my_button2 = ReplyKeyboardMarkup([
                                        ['на главную','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                        # ,[contact_button,location_button]
                                       ], resize_keyboard=True
                                      )
    update.message.reply_text(text, reply_markup = my_button2) # удалить скобку и коменты , reply_markup=my_keyboard)


def send_HotDog_description(bot, update):
    text = 'сосиска в булке c горчичкой и томатным соусом'
    Kor_list = glob('coffee/sweet_hot*.jp*g')
    Kor_pic = choice(Kor_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_Browny_description(bot, update):
    Kor_list = glob('coffee/sweet_b*.jp*g')
    Kor_pic = choice(Kor_list)
    text = 'bakery with lots of chocolate'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_Kozinka_description(bot, update):
    Kor_list = glob('coffee/sweet_k*.jp*g')
    Kor_pic = choice(Kor_list)
    text = 'песочная корзинка с белковым кремом'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_Sharlotka_description(bot, update):
    Kor_list = glob('coffee/sweet_sh*.jp*g')
    Kor_pic = choice(Kor_list)
    text = 'sponge with apples inside and cinnamon on the top'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_Cupcacke_description(bot, update):
    Kor_list = glob('coffee/sweet_c*.jp*g')
    Kor_pic = choice(Kor_list)
    text = 'chocolate cupcake from Marisha'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_Americano_description(bot, update):
    Dan_list = glob('coffee/coffee1*.jp*g')
    Dan_pic = choice(Dan_list)
    text = 'just black coffee'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))


def send_Capuccino_description(bot, update):
    Dan_list = glob('coffee/coffee2*.jp*g')
    Dan_pic = choice(Dan_list)
    text = 'coffee with milk'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))
    return text 



def send_Latte_description(bot, update):
    Dan_list = glob('coffee/coffee3*.jp*g')
    Dan_pic = choice(Dan_list)
    text = 'coffee rich of milk, more than in Capuccino'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))


def send_Glase_description(bot, update):  # без вот этого работает...  , user_data):
    Glase_list = glob('coffee/coffee4*.jp*g')
    Glase_pic = choice(Glase_list)
    text = 'coffee with spoon of ice-cream'
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Glase_pic, 'rb'))

