import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from settings import PROXY
from handlers import start_handler





def main():
    mybot = Updater(os.getenv('API_KEY'), request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start_handler, pass_user_data=True))



if __name__ == '__main__':
    main()