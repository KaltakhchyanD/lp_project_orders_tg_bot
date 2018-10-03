from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters


def start_handler(bot, update, user_data):
    update.message.reply_text(''' Привет, я бот, который поможет
тебе заказать пиццу или выпить кофе!
Выбери опцию, нажав одну из кнопок:''',
         reply_markup = ReplyKeyboardMarkup([['Pizza main menu'],['Cafe main menu']]))




