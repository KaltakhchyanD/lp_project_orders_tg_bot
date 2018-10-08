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


cafe_main_menu_markup = ReplyKeyboardMarkup([['Menu_coffee'],
                                     ['Menu_sweets'],
                                     ['Checkout'],
                                     ['Contact_info']]) 


def cafe_main_menu_handler(bot, update, user_data):
    update.message.reply_text('''Welcome to cafe with nice bakery, 
choose what do you want excactly''',
    reply_markup=cafe_main_menu_markup)
    return 'menu_cafe_state'



def keyboard_coffee(bot, update, user_data):
    update.message.reply_text( 'Выберите кофеёк или вернитесь назад, чтоб выбрать сладость:',
        reply_markup = ReplyKeyboardMarkup([
                                        ['Menu_sweets','корзина'],
                                        ['Americano','Гляссе' ],
                                        ['Capuccino','Latte']
                                        ], resize_keyboard=True
                                        ))
    return 'menu_coffee_bar'


def keyboard_sweets(bot, update, user_data):
    update.message.reply_text( 'Привет, что бы вы хотели из бейкери, из сладенького?',    
    reply_markup = ReplyKeyboardMarkup([
                                        ['menu_coffee_bar','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                       ], resize_keyboard=True
                                      ))
    return 'menu_sweets_bar'


def send_HotDog_description(bot, update, user_data):
    Kor_list = glob('coffee/sweet_hot*.jp*g')
    Kor_pic = choice(Kor_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text('сосиска в булке c горчичкой и томатным соусом',
        reply_markup=ReplyKeyboardMarkup([
                                        ['menu_coffee_bar','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                       ], resize_keyboard=True
                                      ))
    return 'menu_sweets_bar'


def send_Browny_description(bot, update, user_data):
    Brown_list = glob('coffee/sweet_b*.jp*g')
    Brown_pic = choice(Brown_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Brown_pic, 'rb'))
    update.message.reply_text('bakery with lots of chocolate',
        reply_markup=ReplyKeyboardMarkup([
                                        ['menu_coffee_bar','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                       ], resize_keyboard=True
                                      ))
    return 'menu_sweets_bar'


def send_Kozinka_description(bot, update, user_data):
    Kor_list = glob('coffee/sweet_k*.jp*g')
    Kor_pic = choice(Kor_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text('песочная корзинка с белковым кремом', 
        reply_markup=ReplyKeyboardMarkup([
                                        ['menu_coffee_bar','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                       ], resize_keyboard=True
                                      ))
    return 'menu_sweets_bar'


def send_Sharlotka_description(bot, update, user_data):
    Kor_list = glob('coffee/sweet_sh*.jp*g')
    Kor_pic = choice(Kor_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text('sponge with apples inside and cinnamon on the top', 
        reply_markup=ReplyKeyboardMarkup([
                                        ['menu_coffee_bar','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                       ], resize_keyboard=True
                                      ))
    return 'menu_sweets_bar'



def send_Cupcacke_description(bot, update, user_data):
    Kor_list = glob('coffee/sweet_c*.jp*g')
    Kor_pic = choice(Kor_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
    update.message.reply_text( 'chocolate cupcake from Marisha', 
        reply_markup=ReplyKeyboardMarkup([
                                        ['menu_coffee_bar','корзина'],
                                        ['Browny','hot dog' , 'chocupcake'],
                                        ['шарлотку','корзиночку']
                                       ], resize_keyboard=True
                                      ))
    return 'menu_sweets_bar'


def send_Americano_description(bot, update, user_data):
    Dan_list = glob('coffee/coffee1*.jp*g')
    Dan_pic = choice(Dan_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))
    update.message.reply_text( 'just black coffee',
        reply_markup = ReplyKeyboardMarkup([
                                        ['Menu_sweets','корзина'],
                                        ['Americano','Гляссе' ],
                                        ['Capuccino','Latte']
                                        ], resize_keyboard=True
                                        ))
    return 'menu_coffee_bar'


def send_Capuccino_description(bot, update, user_data):
    Dan_list = glob('coffee/coffee2*.jp*g')
    Dan_pic = choice(Dan_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))
    update.message.reply_text( 'coffee with milk',
        reply_markup = ReplyKeyboardMarkup([
                                        ['Menu_sweets','корзина'],
                                        ['Americano','Гляссе' ],
                                        ['Capuccino','Latte']
                                        ], resize_keyboard=True
                                        ))
    return 'menu_coffee_bar'



def send_Latte_description(bot, update, user_data):
    Lat_list = glob('coffee/coffee3*.jp*g')
    Lat_pic = choice(Lat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Lat_pic, 'rb'))
    update.message.reply_text( 'coffee rich of milk, more than in Capuccino',
        reply_markup = ReplyKeyboardMarkup([
                                        ['Menu_sweets','корзина'],
                                        ['Americano','Гляссе' ],
                                        ['Capuccino','Latte']
                                        ], resize_keyboard=True
                                        ))
    return 'menu_coffee_bar'


def send_Glase_description(bot, update, user_data):
    Glase_list = glob('coffee/coffee4*.jp*g')
    Glase_pic = choice(Glase_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(Glase_pic, 'rb'))
    update.message.reply_text( 'coffee with spoon of ice-cream',
        reply_markup = ReplyKeyboardMarkup([
                                        ['Menu_sweets','корзина'],
                                        ['Americano','Гляссе' ],
                                        ['Capuccino','Latte']
                                        ], resize_keyboard=True
                                        ))
    return 'menu_coffee_bar'
