import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from handlers import conversation
from settings import PROXY
from settings import API_KEY

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
#                    filename='bot.log'
                    )

logger = logging.getLogger(__name__)
logger.info('BOT-BOT')



def main():
    mybot = Updater(API_KEY, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(conversation)


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()